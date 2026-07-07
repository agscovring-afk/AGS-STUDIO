from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Supplier:
    id: Optional[int] = None
    company_id: Optional[int] = None
    code: str = ""
    name: str = ""
    contact: str = ""
    phone: str = ""
    mobile: str = ""
    email: str = ""
    address: str = ""
    city: str = ""
    wilaya: str = ""
    country: str = ""
    postal_code: str = ""
    rc: str = ""
    nif: str = ""
    nis: str = ""
    ai: str = ""
    bank: str = ""
    rib: str = ""
    notes: str = ""
    status: str = "active"
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
