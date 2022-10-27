import re

import pytest


def assert_no_text_match_in_lines(pattern, lines):
    """Helper function to check that a given pattern is not present in a list of lines

    :param str pattern: the regex to pattern to check for
    :param list[str] lines: the list of lines to check

    :returns: None
    :raises AssertionError: if the pattern is found in the list of lines
    """
    r = re.compile(pattern)
    if any(r.match(line) for line in lines):
        assert False, (
            "Did not expect to have a line matching %s in the following text:\n%s" % (
                pattern,
                "\n".join(lines),
            )
        )


def assert_only_expected_tests_collected(test_result, expected, not_expected):
    """Helper function to check that correct tests were collected

    :param pytest.pytester.RunResult result: the result of the test session
    :param list[str] expected: the list of tests that are expected to have been run
    :param list[str] not_expected: the list of tests that are not expected to have been
        run

    :returns: None
    :raises AssertionError: if there is a mismatch between expected tests and the result
        of the test session
    """
    test_result.assert_outcomes(passed=len(expected))
    test_result.stdout.fnmatch_lines(["*%s*" % test_name for test_name in expected])
    for test_name in not_expected:
        assert_no_text_match_in_lines(".*%s.*" % test_name, test_result.outlines)


@pytest.fixture
def test_names():
    """Fixture for dummy test names"""
    return [
        "test_one",
        "test_two",
        "test_three",
    ]


@pytest.fixture(autouse=True)
def example_test(testdir, test_names):
    """Example test file with Allure markers"""
    testdir.makepyfile(
        """
        import allure

        @allure.epic("Epic1")
        @allure.feature("Feature1")
        @allure.story("Story1")
        def {test_name_1}():
            pass

        @allure.epic("Epic1")
        @allure.feature("Feature2")
        @allure.story("Story1")
        def {test_name_2}():
            pass

        @allure.epic("Epic2")
        @allure.feature("Feature1")
        @allure.story("Story1")
        def {test_name_3}():
            pass
        """.format(
            test_name_1=test_names[0],
            test_name_2=test_names[1],
            test_name_3=test_names[2],
        )
    )


class TestSingleSelectionIsNotBroken(object):
    """Tests that check that selecting tests with a single flag works

    This makes sure that the simplest behavior defined by the allure-pytest plugin is not
    broken by the pytest-allure-intersection plugin.
    """

    @staticmethod
    def test_selection_epic_only(testdir, test_names):
        result = testdir.runpytest(
            "--allure-selection-by-intersection",
            "--allure-epics=Epic1",
            "-v",
        )
        assert_only_expected_tests_collected(
            result,
            expected=[test_names[0], test_names[1]],
            not_expected=[test_names[2]],
        )

    @staticmethod
    def test_selection_feature_only(testdir, test_names):
        result = testdir.runpytest(
            "--allure-selection-by-intersection",
            "--allure-features=Feature1",
            "-v",
        )
        assert_only_expected_tests_collected(
            result,
            expected=[test_names[0], test_names[2]],
            not_expected=[test_names[1]],
        )


def test_selection_intersection_non_empty(testdir, test_names):
    result = testdir.runpytest(
        "--allure-selection-by-intersection",
        "--allure-epics=Epic1",
        "--allure-features=Feature1",
        "-v",
    )
    assert_only_expected_tests_collected(
        result,
        expected=[test_names[0]],
        not_expected=[test_names[1], test_names[2]],
    )


def test_selection_intersection_empty(testdir, test_names):
    result = testdir.runpytest(
        "--allure-selection-by-intersection",
        "--allure-epics=Epic2",
        "--allure-features=Feature2",
        "-v",
    )
    assert_only_expected_tests_collected(
        result,
        expected=[],
        not_expected=test_names,
    )


def test_selection_old_behavior(testdir, test_names):
    result = testdir.runpytest(
        "--allure-epics=Epic1",
        "--allure-features=Feature1",
        "-v",
    )
    assert_only_expected_tests_collected(
        result,
        expected=test_names,
        not_expected=[],
    )
