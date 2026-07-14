from pathlib import Path


class CodeWriter:

    def write(self, module, section, content, extension):

        base = Path("generated") / module / section
        base.mkdir(parents=True, exist_ok=True)

        filename = f"{module}.{extension}"
        file = base / filename

        file.write_text(content, encoding="utf8")

        return {
            "status": "written",
            "file": str(file)
        }
