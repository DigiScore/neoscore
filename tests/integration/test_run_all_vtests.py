import os
import pathlib
import re
import subprocess

import pytest

vtest_dir = (pathlib.Path(__file__).parent / ".." / ".." / "vtests").resolve()
vtest_dir_contents = os.listdir(vtest_dir)
vtest_file_names = [
    f
    for f in vtest_dir_contents
    if f.endswith(".py")
    and f not in ["helpers.py", "repl.py", "animation.py", "pdf.py"]
]


@pytest.mark.parametrize("file_name", vtest_file_names)
def test_vtests(file_name: str):
    validate_script_safe_to_run(file_name)
    subprocess.run(
        ["python", file_name, "--image", "--tmp", "--automated"],
        cwd=vtest_dir,
        check=True,
    )


def test_pdf_vtest():
    file_name = "pdf.py"
    validate_script_safe_to_run(file_name)
    subprocess.run(
        ["python", file_name, "--pdf", "--tmp", "--automated"],
        cwd=vtest_dir,
        check=True,
    )


def validate_script_safe_to_run(file_name: str):
    script = (vtest_dir / file_name).read_text()
    assert re.search(r"neoscore.show\(.*?\)", script) is None
    assert re.search(r"render_vtest\(.*?\)", script) is not None
