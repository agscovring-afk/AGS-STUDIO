
from pathlib import Path


class ProfessionalMainWindowGenerationEngine:

    def __init__(self):
        self.base = Path("app/builders/professional_main_window")

    def run(self):

        print("=" * 80)
        print("AGS ERP V3 PROFESSIONAL MAIN WINDOW GENERATION ENGINE V1")
        print("=" * 80)

        builders = [
            ("Layout", "layout_builder.py"),
            ("Sidebar", "sidebar_builder.py"),
            ("Toolbar", "toolbar_builder.py"),
            ("Workspace", "workspace_builder.py"),
            ("Dashboard", "dashboard_builder.py"),
            ("Pages", "pages_builder.py"),
            ("Router", "router_builder.py"),
            ("SQLite Binding", "sqlite_binding_builder.py"),
        ]

        result = []

        for name, file in builders:
            path = self.base / file

            if path.exists():
                result.append(
                    {
                        "component": name,
                        "status": "READY",
                        "file": str(path)
                    }
                )
            else:
                result.append(
                    {
                        "component": name,
                        "status": "MISSING",
                        "file": str(path)
                    }
                )

        print("-" * 80)

        for item in result:
            print(
                f"[{item['status']}] "
                f"{item['component']} -> {item['file']}"
            )

        print("-" * 80)

        if all(x["status"] == "READY" for x in result):
            print("[SUCCESS] PROFESSIONAL MAIN WINDOW GENERATION ENGINE V1 READY")
            return True

        print("[FAILED] ENGINE VALIDATION FAILED")
        return False


if __name__ == "__main__":
    ProfessionalMainWindowGenerationEngine().run()
