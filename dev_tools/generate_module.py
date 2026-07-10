"""
AGS ERP V2
Module Generator
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"


FOLDERS = [
    "models",
    "repositories",
    "controllers",
    "services",
    "ui/pages",
]


TEMPLATES = {
    "model": """from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class {ClassName}:
    id: Optional[int] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
""",

    "repository": """from app.repositories.base_repository import BaseRepository


class {ClassName}Repository(BaseRepository):

    def __init__(self, db_path=None):
        super().__init__(db_path)
""",

    "controller": """from app.repositories.{module}_repository import {ClassName}Repository


class {ClassName}Controller:

    def __init__(self, repo:{ClassName}Repository):
        self.repo = repo
""",

    "service": """class {ClassName}Service:
    pass
""",

    "page": """import tkinter as tk


class {ClassName}Page(tk.Frame):

    def __init__(self,parent):
        super().__init__(parent)
"""
}


def create_module(name):

    module = name.lower()

    classname = name.capitalize()

    files = {
        APP / "models" / f"{module}.py":
            TEMPLATES["model"],

        APP / "repositories" / f"{module}_repository.py":
            TEMPLATES["repository"],

        APP / "controllers" / f"{module}_controller.py":
            TEMPLATES["controller"],

        APP / "services" / f"{module}_service.py":
            TEMPLATES["service"],

        APP / "ui/pages" / f"{module}_page.py":
            TEMPLATES["page"],
    }

    for path, template in files.items():

        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            print(f"SKIP : {path.name}")
            continue

        path.write_text(
            template.format(
                module=module,
                ClassName=classname,
            ),
            encoding="utf-8",
        )

        print(f"OK   : {path.name}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python dev_tools/generate_module.py Client")
        sys.exit()

    create_module(sys.argv[1])