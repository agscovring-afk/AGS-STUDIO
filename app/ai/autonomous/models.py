"""
app/ai/autonomous/models.py
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field


class TaskStatus(str, Enum):

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:

    name: str

    description: str = ""

    priority: int = 5

    status: TaskStatus = TaskStatus.PENDING

    retries: int = 0

    max_retries: int = 3

    result: dict = field(
        default_factory=dict
    )


@dataclass
class FileInfo:

    path: str

    extension: str

    size: int = 0