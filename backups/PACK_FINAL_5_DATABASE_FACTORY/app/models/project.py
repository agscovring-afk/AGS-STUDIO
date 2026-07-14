from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    id: Optional[int] = None
    company_id: Optional[int] = None
    code: str = ""
    name: str = ""
    client_id: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    actual_end: Optional[str] = None
    status: str = "planned"
    budget: float = 0.0
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
