
from app.models.base_model import BaseModel


class Clients(BaseModel):

    table_name = "clients"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
