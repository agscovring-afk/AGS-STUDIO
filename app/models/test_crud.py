
from app.models.base_model import BaseModel


class TestCrud(BaseModel):

    table_name = "test_crud"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
