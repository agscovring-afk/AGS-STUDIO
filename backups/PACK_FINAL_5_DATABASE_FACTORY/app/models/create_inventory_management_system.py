
from app.models.base_model import BaseModel


class CreateInventoryManagementSystem(BaseModel):

    table_name = "create_inventory_management_system"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
