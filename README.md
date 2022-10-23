<p align="center">
  <img src="https://www.dropbox.com/s/yvztjxtcbtw6t6v/pytest-allure-intersection-logo.svg?raw=1" />
</p>
<p align="center" style="font-size:30px;font-weight:bolder;font-family:monospace;font-style:italic">pytest-allure-intersection</p>

## Installation

```bash
> pip install pytest-allure-intersection
```

## Usage

This pytest plugin modifies the selection behavior of Allure selection options.

If you run:

```bash
> pytest --allure-epics=MyGreatEpic --allure-features=MyGreatFeature
```

By default, this command would select all tests that are decorated *either* with `@allure.epic("MyGreatEpic")` or `@allure.feature("MyGreatFeature")`, *i.e.* the selection is based on the *union* of the flags.

After installing the *pytest-allure-intersection* plugin, tests will be selected only if they match *both* criteria, *i.e.* a test is selected if its Allure decorators are a superset of the flags requested on the CLI.

There is nothing to do to use the plugin apart from installing it.

You can restore the default behavior by passing `--allure-selection-by-union`.

## Contributing

*pytest-allure-intersection* uses Poetry for its development. To run tests, use:

```bash
> poetry run tox
```