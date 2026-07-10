"""
app/ai/autonomous/exporter.py
"""

from __future__ import annotations

import json
from pathlib import Path


class AutonomousExporter:

    def __init__(self, path="reports/autonomous_doctor.json"):

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


    def export(self, data):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return str(self.path)