"""
AGS Autonomous V2
Project Scanner
"""

from __future__ import annotations

from pathlib import Path


class ProjectScanner:


    EXCLUDED = {

        ".git",
        ".venv",
        ".venv-1",
        "__pycache__",
        ".pytest_cache",
        ".idea",
        ".vscode",
        "node_modules",
        "dist",
        "build"

    }


    INCLUDED_EXTENSIONS = {

        ".py",
        ".json",
        ".yaml",
        ".yml",
        ".md"

    }


    def __init__(self, context):

        self.context = context

        self.root = Path.cwd()



    def scan(self):

        files = []

        for path in self.root.rglob("*"):


            if not path.is_file():
                continue


            if any(
                part in self.EXCLUDED
                for part in path.parts
            ):
                continue


            if path.suffix not in self.INCLUDED_EXTENSIONS:
                continue


            files.append(
                str(path)
            )


        self.context.snapshot.files = files

        self.context.save()


        return {

            "files": len(files),

            "excluded": list(
                self.EXCLUDED
            )

        }
