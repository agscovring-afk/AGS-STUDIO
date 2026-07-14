"""
app/ai/autonomous/memory.py
"""

from __future__ import annotations

import json
from pathlib import Path


class AutonomousMemory:

    def __init__(self, path="data/autonomous_memory.json"):
        self.path = Path(path)
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(self, data):

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

    def load(self):

        if not self.path.exists():
            return {}

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    def remember(self, key, value):

        memory = self.load()

        memory[key] = value

        self.save(memory)

        return True