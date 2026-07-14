"""
AGS ERP V2
Session Context
"""


class Session:

    _user = None
    _company = None
    _permissions = []

    @classmethod
    def set_user(cls, user):
        cls._user = user

    @classmethod
    def get_user(cls):
        return cls._user

    @classmethod
    def set_company(cls, company):
        cls._company = company

    @classmethod
    def get_company(cls):
        return cls._company

    @classmethod
    def set_permissions(cls, permissions):
        cls._permissions = permissions

    @classmethod
    def has_permission(cls, permission):
        return permission in cls._permissions

    @classmethod
    def clear(cls):
        cls._user = None
        cls._company = None
        cls._permissions = []