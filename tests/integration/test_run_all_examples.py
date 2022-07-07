import os
import pathlib
import re
import subprocess
import sys
from typing import List

import pytest

example_dir = (pathlib.Path(__file__).parent / ".." / ".." / "examples").resolve()
example_dir_contents: List[str] = os.listdir(example_dir)
example_script_paths = [
    example_dir / f
    for f in example_dir_contents
    if f.endswith(".py")
    and f not in ["helpers.py", "repl.py", "animation.py", "pdf.py"]
]
example_script_paths.append(example_dir / "feldman_projection_2" / "main.py")


@pytest.mark.parametrize("file_name", example_script_paths)
def test_examples(file_name: str):
    validate_script_safe_to_run(file_name)
    subprocess.run(
        [sys.executable, file_name, "--image", "--tmp", "--automated"],
        cwd=example_dir,
        check=True,
    )


def test_pdf_example():
    file_name = "pdf.py"
    validate_script_safe_to_run(file_name)
    subprocess.run(
        [sys.executable, file_name, "--pdf", "--tmp", "--automated"],
        cwd=example_dir,
        check=True,
    )


def validate_script_safe_to_run(file_name: str):
    script = (example_dir / file_name).read_text()
    assert re.search(r"neoscore.show\(.*?\)", script) is None
    assert re.search(r"render_example\(.*?\)", script) is not None
