from pathlib import Path
import json
from datetime import datetime


class EnterpriseGenerator:

    def __init__(self):
        self.root = Path("enterprise_output")


    def create(self):
        self.root.mkdir(exist_ok=True)

        return {
            "status": "created",
            "path": str(self.root)
        }
