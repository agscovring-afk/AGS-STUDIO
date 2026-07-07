"""Company model + basic schema helper."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Company:
    id: Optional[int] = None
    legal_name: str = ""
    commercial_name: str = ""
    code: str = ""
    currency: str = "DZD"
    language: str = "fr"
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
