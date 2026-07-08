
from app.models.base_model import BaseModel


class TestMemory(BaseModel):

    table_name = "test_memory"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
