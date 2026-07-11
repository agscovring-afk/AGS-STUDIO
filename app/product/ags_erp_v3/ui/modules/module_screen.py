from datetime import datetime


class ModuleScreen:

    def __init__(self, name):
        self.name = name
        self.created_at = datetime.now()

    def render(self):
        return {
            "module": self.name,
            "status": "READY",
            "screen": f"AGS ERP V3 {self.name} SCREEN"
        }
