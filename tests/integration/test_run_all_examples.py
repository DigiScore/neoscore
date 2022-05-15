import os
import pathlib
import re
import subprocess

import pytest

example_dir = (pathlib.Path(__file__).parent / ".." / ".." / "examples").resolve()
example_dir_contents: list[str] = os.listdir(example_dir)
example_file_names = [
    f
    for f in example_dir_contents
    if f.endswith(".py")
    and f not in ["helpers.py", "repl.py", "animation.py", "pdf.py"]
]


@pytest.mark.parametrize("file_name", example_file_names)
def test_examples(file_name: str):
    validate_script_safe_to_run(file_name)
    subprocess.run(
        ["python", file_name, "--image", "--tmp", "--automated"],
        cwd=example_dir,
        check=True,
    )


def test_pdf_example():
    file_name = "pdf.py"
    validate_script_safe_to_run(file_name)
    subprocess.run(
        ["python", file_name, "--pdf", "--tmp", "--automated"],
        cwd=example_dir,
        check=True,
    )


def validate_script_safe_to_run(file_name: str):
    script = (example_dir / file_name).read_text()
    assert re.search(r"neoscore.show\(.*?\)", script) is None
    assert re.search(r"render_example\(.*?\)", script) is not None
