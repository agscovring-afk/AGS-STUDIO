from .base_agent import BaseAgent
from pathlib import Path
import json

EXCLUDED = {
    "__pycache__",".git",".venv","venv","env",
    "build","dist",".pytest_cache",".mypy_cache"
}

class ArchitectAgent(BaseAgent):

    name = "architect_agent"
    role = "system architecture designer"

    def execute(self, task):

        self.log("Building Project Inventory")

        root = Path(self.context if isinstance(self.context, str) else ".").resolve()

        inventory = {
            "project_root": str(root),
            "packages": [],
            "modules": [],
            "python_files": [],
            "entry_points": [],
            "configs": []
        }

        for f in root.rglob("*"):

            if any(p in EXCLUDED for p in f.parts):
                continue

            if f.is_dir():

                if (f / "__init__.py").exists():
                    inventory["packages"].append(str(f.relative_to(root)))

                continue

            if f.suffix == ".py":

                rel = str(f.relative_to(root))

                inventory["python_files"].append(rel)

                inventory["modules"].append(
                    rel.replace("\\",".").replace("/",".")[:-3]
                )

                if f.name in (
                    "main.py",
                    "master.py",
                    "runtime.py",
                    "__main__.py"
                ):
                    inventory["entry_points"].append(rel)

            elif f.suffix.lower() in (
                ".json",".yaml",".yml",".toml",".ini",".cfg"
            ):
                inventory["configs"].append(str(f.relative_to(root)))

        out = root / "data" / "project_inventory.json"
        out.parent.mkdir(exist_ok=True)

        out.write_text(
            json.dumps(inventory, indent=4),
            encoding="utf-8"
        )

        return {
            "status":"completed",
            "packages":len(inventory["packages"]),
            "modules":len(inventory["modules"]),
            "python_files":len(inventory["python_files"]),
            "entry_points":len(inventory["entry_points"]),
            "configs":len(inventory["configs"]),
            "inventory":str(out)
        }
