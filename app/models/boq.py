from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class BOQ:
    id: Optional[int] = None
    project_id: Optional[int] = None
    code: str = ""
    title: str = ""
    description: str = ""
    revision: int = 1
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
