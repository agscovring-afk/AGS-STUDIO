"""
AGS ERP V2
Client Model
"""

from datetime import datetime


class Client:

    def __init__(
        self,
        name,
        contact=None,
        function=None,
        phone=None,
        mobile=None,
        email=None,
        address=None,
        city=None,
        wilaya=None,
        country=None,
        rc=None,
        nif=None,
        nis=None,
        ai=None,
        bank=None,
        rib=None
    ):

        self.code = None

        self.name = name
        self.contact = contact
        self.function = function

        self.phone = phone
        self.mobile = mobile

        self.email = email

        self.address = address
        self.city = city
        self.wilaya = wilaya
        self.country = country

        self.rc = rc
        self.nif = nif
        self.nis = nis
        self.ai = ai

        self.bank = bank
        self.rib = rib

        self.company_id = None

        self.status = "active"
        self.is_active = 1

        now = datetime.now()

        self.created_at = now
        self.updated_at = now
