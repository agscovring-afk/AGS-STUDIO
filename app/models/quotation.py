from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Quotation:
    id: Optional[int] = None
    company_id: Optional[int] = None
    code: str = ""
    client_id: Optional[int] = None
    project_id: Optional[int] = None
    date: Optional[str] = None
    validity_date: Optional[str] = None
    status: str = "draft"
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
