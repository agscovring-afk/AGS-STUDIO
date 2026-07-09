from pathlib import Path


class ModuleValidator:

    def validate(self,module):

        module = module.lower()

        base = Path("generated") / module

        required = [

            f"metadata/{module}.json",

            f"models/{module}.py",

            "database/migration.sql",

            f"services/{module}_service.py",

            f"api/{module}_api.py",

            f"ui/{module}_window.py",

            f"ui/{module}.ui"

        ]

        report = []

        ok = True

        for file in required:

            exists = (base / file).exists()

            report.append({

                "file": file,

                "exists": exists

            })

            if not exists:

                ok = False

        return {

            "status": "success" if ok else "failed",

            "files": report

        }
