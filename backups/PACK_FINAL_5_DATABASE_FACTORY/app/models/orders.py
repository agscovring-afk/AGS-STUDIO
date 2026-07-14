
from app.models.base_model import BaseModel


class Orders(BaseModel):

    table_name = "orders"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
