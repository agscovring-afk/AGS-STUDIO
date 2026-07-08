from pathlib import Path
import subprocess
import json


class UpgradeEngine:

    def __init__(self):

        self.root = Path.cwd()

        self.modules = []

        self.report_data = {
            "status": "OK",
            "modules": [],
            "metadata_created": [],
            "pages_found": 0
        }

        self.steps = [
            ("Discover Pages", self.discover_pages),
            ("Metadata Engine", self.metadata),
            ("Schema Engine", self.schema),
            ("Module Generator", self.generator),
            ("UI Generator", self.ui),
            ("CRUD Engine", self.crud),
            ("Router", self.router),
            ("Menu", self.menu),
            ("Validator", self.validator),
            ("Report", self.report),
        ]


    def run(self):

        print()
        print("===================================")
        print(" AGS-STUDIO UPGRADE ENGINE")
        print("===================================")
        print()

        total = len(self.steps)

        for i, (name, func) in enumerate(self.steps, start=1):

            print(f"[{i}/{total}] {name:<25}", end="")

            try:

                func()

                print(" OK")

            except Exception as e:

                print(" FAILED")
                print(e)

                self.report_data["status"] = "FAILED"

                self.report()

                return False

        print()
        print("Upgrade completed successfully.")

        return True


    # ====================================

    def discover_pages(self):

        pages = self.root / "app" / "ui" / "pages"

        for file in pages.glob("*_page.py"):

            module = file.stem.replace("_page", "")

            self.modules.append(module)

        self.report_data["pages_found"] = len(self.modules)


    # ====================================

    def metadata(self):

        folder = self.root / "app" / "metadata" / "modules"

        folder.mkdir(parents=True, exist_ok=True)

        for module in self.modules:

            file = folder / f"{module}.json"

            if not file.exists():

                data = {

                    "module": module,

                    "table": module,

                    "fields": [

                        {

                            "name": "id",

                            "type": "INTEGER",

                            "primary_key": True

                        }

                    ]

                }

                with open(
                    file,
                    "w",
                    encoding="utf-8"
                ) as f:

                    json.dump(
                        data,
                        f,
                        indent=4
                    )

                self.report_data["metadata_created"].append(module)

            self.report_data["modules"].append(module)


    # ====================================

    def schema(self):

        (self.root / "app" / "schema").mkdir(
            exist_ok=True
        )


    def generator(self):

        return


    def ui(self):

        return


    def crud(self):

        return


    # ====================================

    def router(self):

        subprocess.run(

            [

                "python",

                "-c",

                "from app.registry.page_registry import save_registry; save_registry()"

            ],

            check=False

        )


    def menu(self):

        subprocess.run(

            [

                "python",

                "-c",

                "from app.registry.menu_generator import generate_menu; generate_menu()"

            ],

            check=False

        )


    def validator(self):

        return


    # ====================================

    def report(self):

        with open(

            self.root / "upgrade_report.json",

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                self.report_data,

                f,

                indent=4

            )