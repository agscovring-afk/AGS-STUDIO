
from app.models.base_model import BaseModel


class Invoices(BaseModel):

    table_name = "invoices"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
