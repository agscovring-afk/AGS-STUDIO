from dataclasses import dataclass, field
from typing import List


@dataclass
class BuildTask:

    name: str

    agent: str

    payload: dict = field(default_factory=dict)

    depends_on: List[str] = field(default_factory=list)

    status: str = "pending"


@dataclass
class BuildPhase:

    name: str

    tasks: List[BuildTask] = field(default_factory=list)

    status: str = "pending"
