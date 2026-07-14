
from app.models.base_model import BaseModel


class Products(BaseModel):

    table_name = "products"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
