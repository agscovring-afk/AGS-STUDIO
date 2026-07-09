from dataclasses import dataclass
from datetime import datetime


@dataclass
class Inventory:

    id: int | None = None

    code: str = ""

    name: str = ""

    description: str = ""

    active: bool = True

    created_at: datetime | None = None

    updated_at: datetime | None = None
