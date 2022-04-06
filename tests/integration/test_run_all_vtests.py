import os
import pathlib
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


@pytest.mark.parametrize("vtest_path", vtest_file_names)
def test_vtests(vtest_path: str):
    subprocess.run(
        ["python", vtest_path, "--image", "--tmp"], cwd=vtest_dir, check=True
    )


# If/when PDF export can be sped up this should be re-enabled
@pytest.mark.skip(reason="Too slow")
def test_pdf_vtest():
    subprocess.run(["python", "pdf.py", "--pdf", "--tmp"], cwd=vtest_dir, check=True)
