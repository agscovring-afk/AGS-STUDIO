from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Unit:
    id: Optional[int] = None
    name: str = ""
    symbol: str = ""
    conversion_factor: float = 1.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
