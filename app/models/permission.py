from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Permission:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
