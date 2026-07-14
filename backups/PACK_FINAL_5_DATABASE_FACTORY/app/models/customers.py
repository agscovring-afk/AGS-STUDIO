
from app.models.base_model import BaseModel


class Customers(BaseModel):

    table_name = "customers"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
