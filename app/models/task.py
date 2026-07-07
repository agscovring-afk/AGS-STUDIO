from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    id: Optional[int] = None
    project_id: Optional[int] = None
    title: str = ""
    description: str = ""
    assignee_id: Optional[int] = None
    due_date: Optional[str] = None
    priority: str = "normal"
    status: str = "todo"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
