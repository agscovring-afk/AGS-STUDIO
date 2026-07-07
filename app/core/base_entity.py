"""
AGS ERP V2
Base Entity
"""

from datetime import datetime


class BaseEntity:

    def __init__(
        self,
        id=None,
        company_id=None,
        created_at=None,
        updated_at=None,
        is_active=True
    ):
        self.id = id
        self.company_id = company_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.is_active = is_active

    def activate(self):
        self.is_active = True
        self.touch()

    def deactivate(self):
        self.is_active = False
        self.touch()

    def touch(self):
        self.updated_at = datetime.now()