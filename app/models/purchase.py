from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Purchase:
    id: Optional[int] = None
    company_id: Optional[int] = None
    code: str = ""
    supplier_id: Optional[int] = None
    date: Optional[str] = None
    status: str = "draft"
    total: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
