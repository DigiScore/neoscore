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
10. Install the pre-commit hook with `sh dev_scripts/install_pre_commit_hook.sh`

## Running tests

The automated test suite is run using [pytest](https://docs.pytest.org/). Simply call `pytest` to run the suite. The suite can be run much faster in parallel with `pytest -n auto`.

Several visual tests ("vtests") are included which are used to run neoscore programs end-to-end, allowing manual visual inspection. The kitchen sink test is found at `vtests/vtest.py`. If your change has effects on rendered outputs, please verify its correctness on any applicable vtests, adding new tests or code to them if needed.

## Committing

The pre-commit hook, installed with the above-mentioned script, will automatically apply formatting and import corrections. The script will not automatically add them to your commit, since this can be dangerous, so if any changes are added please add and commit them yourself before opening a PR. You can also manually run these hooks before committing with `sh dev_scripts/pre_commit.sh` to prevent double or amended commits. PRs which fail these checks will not build successfully.
