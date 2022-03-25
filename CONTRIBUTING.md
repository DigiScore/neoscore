# Contributor's guide

## Environment setup

1. Clone this repo
2. Ensure python >= 3.10 is available on your system (it doesn't need to be the default installation)
3. Install [poetry](https://python-poetry.org)
4. Navigate your shell to the project direction
5. Run `poetry env use 3.10` to create a Python virtual environment
6. Run `poetry install` to install dependencies in the environment
7. Run `poetry shell` to shell into the virtual environment
8. Run `sh dev_scripts/install_devtools.sh` to install dependencies used to enforce code standards.
9. Test your environment by running `python vtests/vtest.py`

If for some reason you can't get `poetry` working in your environment, you can install from the `requirements.txt` file provided, which includes both dev and prod dependencies.

## Running tests

The automated test suite is run using [pytest](https://docs.pytest.org/). Simply call `pytest` to run the suite. The suite can be run much faster in parallel with `pytest -n auto`.

Several visual tests ("vtests") are included which are used to run neoscore programs end-to-end, allowing manual visual inspection. The kitchen sink test is found at `vtests/vtest.py`. If your change has effects on rendered outputs, please verify its correctness on any applicable vtests, adding new tests or code to them if needed.

## Committing

Before committing, please be sure to run the code standards script with `sh dev_scripts/pre-commit.sh`. This will format your code and clean up imports automatically.

