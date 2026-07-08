
from app.models.base_model import BaseModel


class Suppliers(BaseModel):

    table_name = "suppliers"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
