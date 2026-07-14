"""
AGS ERP V2
Company Model
"""

from app.core.base_entity import BaseEntity


class Company(BaseEntity):

    def __init__(
        self,
        name,
        commercial_name=None,
        phone=None,
        email=None,
        address=None,
        rc=None,
        nif=None,
        nis=None,
        ai=None,
        currency="DZD",
        language="fr",
        **kwargs
    ):

        super().__init__(**kwargs)

        self.code = None
        self.name = name
        self.commercial_name = commercial_name

        self.phone = phone
        self.email = email
        self.address = address

        self.rc = rc
        self.nif = nif
        self.nis = nis
        self.ai = ai

        self.currency = currency
        self.language = language

    def set_code(self, code):
        self.code = code

    def update_contact(
        self,
        phone=None,
        email=None,
        address=None
    ):
        self.phone = phone or self.phone
        self.email = email or self.email
        self.address = address or self.address
        self.touch()