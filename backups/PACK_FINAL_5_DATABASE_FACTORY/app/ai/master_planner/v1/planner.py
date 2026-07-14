from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
import time


@dataclass
class Task:
    name: str
    agent: str
    payload: Any = None
    status: str = "pending"
    started_at: float = 0.0
    finished_at: float = 0.0
    result: Any = None
    error: Optional[str] = None


@dataclass
class Phase:
    name: str
    tasks: List[Task] = field(default_factory=list)
    status: str = "pending"


class MasterPlanner:

    def __init__(self):

        self._phases: List[Phase] = []

        self._agents: Dict[str, Callable[[Task], Any]] = {}

    # --------------------------------------------------

    def register_agent(
        self,
        name: str,
        executor: Callable[[Task], Any],
    ):

        self._agents[name.lower()] = executor

    # --------------------------------------------------

    def add_phase(
        self,
        name: str,
    ) -> Phase:

        phase = Phase(name=name)

        self._phases.append(
            phase
        )

        return phase

    # --------------------------------------------------

    def add_task(
        self,
        phase: Phase,
        name: str,
        agent: str,
        payload: Any = None,
    ):

        phase.tasks.append(
            Task(
                name=name,
                agent=agent,
                payload=payload,
            )
        )

    # --------------------------------------------------

    def phase(
        self,
        name: str,
    ) -> Optional[Phase]:

        for p in self._phases:

            if p.name == name:

                return p

        return None

    # --------------------------------------------------

    def execute(self):

        report = []

        for phase in self._phases:

            print()

            print("=" * 60)

            print(
                f"PHASE : {phase.name}"
            )

            print("=" * 60)

            phase.status = "running"

            for task in phase.tasks:

                task.started_at = time.time()

                task.status = "running"

                print(
                    f"[RUN] {task.name}"
                )

                executor = self._agents.get(
                    task.agent.lower()
                )

                if executor is None:

                    task.status = "failed"

                    task.error = (
                        f"Agent '{task.agent}' not registered."
                    )

                    print(task.error)

                    continue

                try:

                    task.result = executor(
                        task
                    )

                    task.status = "completed"

                except Exception as ex:

                    task.status = "failed"

                    task.error = str(ex)

                    print(
                        f"[ERROR] {ex}"
                    )

                finally:

                    task.finished_at = time.time()

                report.append(task)

            if any(
                t.status == "failed"
                for t in phase.tasks
            ):

                phase.status = "failed"

            else:

                phase.status = "completed"

        return report

    # --------------------------------------------------

    def summary(self):

        print()

        print("=" * 60)

        print("MASTER PLANNER REPORT")

        print("=" * 60)

        for phase in self._phases:

            completed = len(
                [
                    t
                    for t in phase.tasks
                    if t.status == "completed"
                ]
            )

            failed = len(
                [
                    t
                    for t in phase.tasks
                    if t.status == "failed"
                ]
            )

            print()

            print(
                f"{phase.name}"
            )

            print(
                f"Status    : {phase.status}"
            )

            print(
                f"Completed : {completed}"
            )

            print(
                f"Failed    : {failed}"
            )

        print()

        print("=" * 60)

        print("END REPORT")

        print("=" * 60)