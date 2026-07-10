"""
app/ai/autonomous/scanner.py
"""

from __future__ import annotations

from pathlib import Path

from .models import FileInfo


class ProjectScanner:

    def __init__(self, context, root="."):

        self.context = context
        self.root = Path(root)


    def scan(self):

        files = []

        for path in self.root.rglob("*"):

            if not path.is_file():
                continue

            if "__pycache__" in path.parts:
                continue

            try:
                size = path.stat().st_size

            except Exception:

                size = 0


            files.append(
                FileInfo(
                    path=str(path),
                    extension=path.suffix,
                    size=size,
                )
            )


        self.context.snapshot.files = files

        return {
            "files_found": len(files),
        }


    def python_files(self):

        return [
            f
            for f in self.context.snapshot.files
            if f.extension == ".py"
        ]