from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ExpenseCategory:
    id: Optional[int] = None
    company_id: Optional[int] = None
    name: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
