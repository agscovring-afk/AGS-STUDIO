"""
app/ai/autonomous/context.py
"""

from __future__ import annotations

import json
from pathlib import Path


class AutonomousSnapshot:

    def __init__(self):

        self.tasks = []
        self.statistics = {}


    @property
    def pending_tasks(self):

        return [
            t for t in self.tasks
            if getattr(t, "status", None) == "pending"
        ]


    @property
    def failed_tasks(self):

        return [
            t for t in self.tasks
            if getattr(t, "status", None) == "failed"
        ]


    @property
    def completed_tasks(self):

        return [
            t for t in self.tasks
            if getattr(t, "status", None) == "completed"
        ]


    @property
    def files(self):

        return []



class AutonomousContext:

    def __init__(self, path="data/autonomous_state.json"):

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.snapshot = AutonomousSnapshot()



    def update_statistics(self):

        self.snapshot.statistics = {

            "tasks": len(self.snapshot.tasks),

            "pending": len(self.snapshot.pending_tasks),

            "failed": len(self.snapshot.failed_tasks),

            "completed": len(self.snapshot.completed_tasks),

        }



    def save(self):

        self.update_statistics()

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.snapshot.statistics,
                file,
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
        ) as file:

            return json.load(file)



    def statistics(self):

        self.update_statistics()

        return self.snapshot.statistics