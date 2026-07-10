from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Employee:
    id: Optional[int] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
