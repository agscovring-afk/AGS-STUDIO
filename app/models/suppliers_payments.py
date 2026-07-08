
from app.models.base_model import BaseModel


class SuppliersPayments(BaseModel):

    table_name = "suppliers_payments"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
