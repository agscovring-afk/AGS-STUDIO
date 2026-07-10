from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Service:
    id: Optional[int] = None
    company_id: Optional[int] = None
    code: str = ""
    name: str = ""
    category_id: Optional[int] = None
    unit_id: Optional[int] = None
    default_price: float = 0.0
    tax_rate: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
