from dataclasses import dataclass, field
from typing import List, Dict, Any

from app.ai.orchestrator.core.step import WorkflowStep


@dataclass
class Workflow:

    name: str

    description: str = ""

    steps: List[WorkflowStep] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


    def add_step(
        self,
        step: WorkflowStep
    ):

        self.steps.append(step)

        return step


    def remove_step(
        self,
        name: str
    ):

        self.steps = [

            s

            for s in self.steps

            if s.name != name

        ]


    def get_step(
        self,
        name: str
    ):

        for step in self.steps:

            if step.name == name:

                return step

        return None


    def has_step(
        self,
        name: str
    ):

        return self.get_step(
            name
        ) is not None


    def clear(self):

        self.steps.clear()


    def count(self):

        return len(
            self.steps
        )


    def to_dict(self):

        return {

            "name": self.name,

            "description": self.description,

            "metadata": self.metadata,

            "steps": [

                step.to_dict()

                for step in self.steps

            ]

        }


    @classmethod
    def from_dict(
        cls,
        data
    ):

        workflow = cls(

            name=data["name"],

            description=data.get(
                "description",
                ""
            ),

            metadata=data.get(
                "metadata",
                {}
            )

        )

        for item in data.get(
            "steps",
            []
        ):

            workflow.add_step(

                WorkflowStep.from_dict(
                    item
                )

            )

        return workflow