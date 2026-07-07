from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class StockLevel:
    id: Optional[int] = None
    product_id: Optional[int] = None
    warehouse_id: Optional[int] = None
    quantity: float = 0.0
    reserved: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
