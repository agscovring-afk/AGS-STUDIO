from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Expense:
    id: Optional[int] = None
    company_id: Optional[int] = None
    category_id: Optional[int] = None
    amount: float = 0.0
    date: Optional[str] = None
    project_id: Optional[int] = None
    supplier_id: Optional[int] = None
    payment_method: str = "cash"
    attachment: Optional[str] = None
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
