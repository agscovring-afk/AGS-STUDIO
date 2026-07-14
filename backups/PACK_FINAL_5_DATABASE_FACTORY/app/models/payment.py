from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Payment:
    id: Optional[int] = None
    invoice_id: Optional[int] = None
    amount: float = 0.0
    date: Optional[str] = None
    method: str = "cash"
    reference: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
