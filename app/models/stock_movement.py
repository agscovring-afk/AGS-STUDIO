from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class StockMovement:
    id: Optional[int] = None
    product_id: Optional[int] = None
    warehouse_from: Optional[int] = None
    warehouse_to: Optional[int] = None
    movement_type: str = "IN"  # IN, OUT, TRANSFER, ADJUSTMENT
    quantity: float = 0.0
    reference: str = ""
    reason: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
