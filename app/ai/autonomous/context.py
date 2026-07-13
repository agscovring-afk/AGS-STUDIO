"""
app/ai/autonomous/context.py
"""

from __future__ import annotations

import json
from pathlib import Path

from app.ai.autonomous.models import Task, TaskStatus


class AutonomousSnapshot:

    def __init__(self):

        self.tasks = []
        self.statistics = {}
        self._files = []


    @property
    def pending_tasks(self):

        return [
            t for t in self.tasks
            if t.status == TaskStatus.PENDING
        ]


    @property
    def failed_tasks(self):

        return [
            t for t in self.tasks
            if t.status == TaskStatus.FAILED
        ]


    @property
    def completed_tasks(self):

        return [
            t for t in self.tasks
            if t.status == TaskStatus.COMPLETED
        ]


    @property
    def files(self):

        return self._files


    @files.setter
    def files(self, value):

        self._files = value



class AutonomousContext:

    def __init__(self, path="data/autonomous_state.json"):

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.snapshot = AutonomousSnapshot()

        self.load()



    def update_statistics(self):

        self.snapshot.statistics = {

            "tasks": len(self.snapshot.tasks),
            "pending": len(self.snapshot.pending_tasks),
            "failed": len(self.snapshot.failed_tasks),
            "completed": len(self.snapshot.completed_tasks),
            "files": len(self.snapshot.files),

        }



    def save(self):

        self.update_statistics()

        data = {

            "tasks": [

                {

                    "name": t.name,
                    "description": t.description,
                    "status": t.status.value,
                    "priority": t.priority,
                    "retries": t.retries,
                    "max_retries": t.max_retries,
                    "result": t.result

                }

                for t in self.snapshot.tasks

            ],

            "statistics": self.snapshot.statistics,

            "files": self.snapshot.files

        }


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



    def load(self):

        if not self.path.exists():

            return {}


        try:

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)


            self.snapshot.tasks = []


            for item in data.get("tasks", []):

                self.snapshot.tasks.append(

                    Task(

                        name=item["name"],

                        status=TaskStatus(
                            item.get(
                                "status",
                                "pending"
                            )
                        ),

                        description=item.get("description", ""),
                        priority=item.get(
                            "priority",
                            1
                        )

                    )

                )


            self.snapshot.statistics = data.get(
                "statistics",
                {}
            )

            self.snapshot.files = data.get(
                "files",
                []
            )


        except Exception:

            self.snapshot = AutonomousSnapshot()



        return self.snapshot



    def statistics(self):

        self.update_statistics()

        return self.snapshot.statistics
