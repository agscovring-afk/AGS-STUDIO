from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class BOQLine:
    id: Optional[int] = None
    boq_id: Optional[int] = None
    line_no: int = 0
    item_type: str = "product"  # product|service
    item_id: Optional[int] = None
    description: str = ""
    quantity: float = 0.0
    unit_id: Optional[int] = None
    unit_price: float = 0.0
    total: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
