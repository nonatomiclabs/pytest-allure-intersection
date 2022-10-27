from allure_pytest.utils import allure_labels


def pytest_addoption(parser):
    parser.addoption(
        "--allure-selection-by-intersection",
        action="store_true", default=False,
        help=(
            "Affects the selection behavior of the allure-pytest plugin by using the "
            "intersection of the requested --allure-xxx flags, instead of the union."
        )
    )


def pytest_collection_modifyitems(items, config):
    if config.option.allure_selection_by_intersection:
        # Get a set of the selection options selected on the command line
        selection_options = set().union(
            config.getoption("allure_epics", default=set()),
            config.getoption("allure_features", default=set()),
            config.getoption("allure_stories", default=set()),
            config.getoption("allure_severities", default=set()),
            config.getoption("allure_ids", default=set()),
        )

        deselected = []
        for index, item in enumerate(items[:]):
            if not allure_labels(item).issuperset(selection_options):
                deselected.append(items.pop(index - len(deselected)))

        config.hook.pytest_deselected(items=deselected)
