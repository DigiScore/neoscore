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
    and f
    not in [
        "animation.py",
        "fractal_score.py",
        "helpers.py",
        "input_scene_interaction.py",
        "input_simple.py",
        "pdf.py",
        "repl.py",
        "transform_origin.py",
        "other_music_fonts.py",
        "inter_process_communication.py",
    ]
]
example_script_paths.append(example_dir / "feldman_projection_2" / "main.py")


@pytest.mark.parametrize("example_path", example_script_paths)
def test_examples(example_path: pathlib.Path):
    validate_script_safe_to_run(example_path)
    subprocess.run(
        [sys.executable, str(example_path), "--image", "--tmp", "--automated"],
        cwd=example_dir,
        check=True,
    )


def test_pdf_example():
    example_file = example_dir / "pdf.py"
    validate_script_safe_to_run(example_file)
    subprocess.run(
        [sys.executable, str(example_file), "--pdf", "--tmp", "--automated"],
        cwd=example_dir,
        check=True,
    )


def validate_script_safe_to_run(example_path: pathlib.Path):
    script = example_path.read_text()
    assert re.search(r"neoscore.show\(.*?\)$", script) is None
    assert re.search(r"render_example\(.*?\)", script) is not None
