import base64
import os
import subprocess
import sys
import tempfile
from hashlib import sha1
from pathlib import Path
from typing import List

from docutils import nodes
from sphinx.directives.code import CodeBlock

DOC_ROOT_DIR = Path(__file__).parent
# Note that these dirs don't respond automatically to config changes
STATIC_RENDER_DIR = DOC_ROOT_DIR / "_build" / "html" / "_static" / "rendered_examples"


class RenderedExample(CodeBlock):
    """Directive for auto-rendering doc examples

    Code examples in ``rendered-example`` RST blocks will automatically be rendered in
    images, identified by their code hashes, and included in the generated HTML below
    the code.

    Neoscore import, setup, and render code is automatically added to examples. Examples
    which need to include these setup bits (useful early in docs for full "hello
    world"-type programs) can disable this behavior by including a ``neoscore.show()``
    call anywhere in the example. When that snippet is detected, this directive only
    replaces that line with an appropriate image export call and leaves the rest of the
    code unchanged.
    """

    def run(self) -> List[nodes.Node]:
        # Run superclass first
        result = super().run()
        # Now render the code block to an image

        # Script ID should be stable across builds for unchanged scripts
        script_id = RenderedExample.hash_script(self.content)
        STATIC_RENDER_DIR.mkdir(parents=True, exist_ok=True)
        export_path = STATIC_RENDER_DIR / (script_id + ".png")
        # If file exists already, that means this code example hasn't
        # changed since last build, so no need to re-render it.
        if not export_path.exists():
            # Add setup and render code to script
            script_lines = list(self.content)
            RenderedExample.post_process_script(script_lines, export_path)
            script_text = "\n".join(script_lines)
            script_file = tempfile.NamedTemporaryFile(
                "w", suffix=".py", delete=False, encoding="utf-8"
            )
            try:
                script_file.write(script_text)
                script_file.flush()
                os.fsync(script_file.fileno())
                script_file.close()
                subprocess.check_call([sys.executable, script_file.name])
            finally:
                script_file.close()
                os.unlink(script_file.name)
        # This hackily assumes exported images live 2 dirs down from root
        # Need to prefix absolute path with TWO slashes due to Sphinx quirk
        # https://github.com/sphinx-doc/sphinx/issues/7772
        image_uri = "//" + "/".join(export_path.parts[-3:])
        image_node = nodes.image(uri=image_uri, classes=["rendered-example"])
        result.append(image_node)
        return result

    @staticmethod
    def hash_script(script: List[str]) -> str:
        """Get a stable hash string unique to a script.

        The given hash string is suitable for use in file paths and URLs.
        """
        merged_script = "\n".join(script)
        h = sha1(merged_script.encode("utf-8")).digest()
        return base64.b32encode(h).decode()

    @staticmethod
    def post_process_script(script: List[str], export_path: Path):
        """Modify `script` in-place preparing it for render"""

        render_line = (
            f"neoscore.render_image("
            + "None,"
            + f"r'{export_path}', 130, autocrop=True)"
        )

        if any(("neoscore.show()" in line for line in script)):
            # Assume script includes setup code too
            # Just overwrite the `show` line with image export
            for i in range(len(script)):
                script[i] = script[i].replace("neoscore.show()", render_line)
        else:
            script.insert(0, "from neoscore.common import *")
            script.insert(1, "neoscore.setup()")
            script.append(render_line)
