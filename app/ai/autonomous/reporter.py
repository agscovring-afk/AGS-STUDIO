"""
app/ai/autonomous/reporter.py
"""

from __future__ import annotations

import json
from pathlib import Path


class AutonomousReporter:

    def __init__(self, path="reports/autonomous_report.json"):

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def generate(self, data):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        return str(self.path)