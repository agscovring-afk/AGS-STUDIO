
from app.models.base_model import BaseModel


class Inventory(BaseModel):

    table_name = "inventory"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
