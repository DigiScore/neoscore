import os
import subprocess
import tempfile
from pathlib import Path
from typing import List

from docutils.nodes import Node
from sphinx.directives.code import CodeBlock

DOC_ROOT_DIR = Path(__file__).parent
# Note that these dirs don't respond automatically to config changes
STATIC_RENDER_DIR = DOC_ROOT_DIR / "_build" / "html" / "_static" / "example_renders"


class RenderedCodeBlock(CodeBlock):
    def run(self) -> List[Node]:
        # Run superclass first
        result = super().run()
        # Now render the code block to an image
        script_file = tempfile.NamedTemporaryFile("w", suffix=".py")
        # Script ID should be stable across builds for unchanged scripts
        # use the hex of the script's hash (stripping leading '0x')
        script_id = hex(hash(tuple(self.content)))[2:]
        STATIC_RENDER_DIR.mkdir(parents=True, exist_ok=True)
        export_path = STATIC_RENDER_DIR / (script_id + ".png")
        # Add setup and render code to script
        script_lines = list(self.content)
        script_lines.insert(0, "from neoscore.common import *")
        script_lines.insert(1, "neoscore.setup()")
        script_lines.append(
            f"neoscore.render_image("
            + "neoscore.document.pages[0].document_space_bounding_rect,"
            + f"'{export_path}', 72, autocrop=True)"
        )
        script_text = "\n".join(script_lines)
        script_file.write(script_text)
        script_file.flush()
        os.fsync(script_file.fileno())
        subprocess.check_call(["python", script_file.name])
        return result
