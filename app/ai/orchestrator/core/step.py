from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class WorkflowStep:

    name: str

    agent: str

    action: str

    enabled: bool = True

    completed: bool = False

    status: str = "pending"

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def start(self):

        self.status = "running"

    def finish(self):

        self.status = "completed"

        self.completed = True

    def fail(self):

        self.status = "failed"

    def reset(self):

        self.status = "pending"

        self.completed = False

    def is_pending(self):

        return self.status == "pending"

    def is_running(self):

        return self.status == "running"

    def is_completed(self):

        return self.status == "completed"

    def is_failed(self):

        return self.status == "failed"

    def to_dict(self):

        return {

            "name": self.name,

            "agent": self.agent,

            "action": self.action,

            "enabled": self.enabled,

            "completed": self.completed,

            "status": self.status,

            "metadata": self.metadata

        }

    @classmethod
    def from_dict(
        cls,
        data
    ):

        return cls(

            name=data["name"],

            agent=data["agent"],

            action=data["action"],

            enabled=data.get(
                "enabled",
                True
            ),

            completed=data.get(
                "completed",
                False
            ),

            status=data.get(
                "status",
                "pending"
            ),

            metadata=data.get(
                "metadata",
                {}
            )

        )