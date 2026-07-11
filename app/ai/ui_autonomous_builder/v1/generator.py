class UIGenerator:

    def generate(self, ui_plan):
        return {
            "files": [
                {
                    "type": "ui",
                    "name": ui_plan.get("module") + "_view.py"
                }
            ],
            "status": "GENERATED"
        }
