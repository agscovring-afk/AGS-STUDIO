
from app.models.test_memory import TestMemory


class TestMemoryRepository:

    model = TestMemory


    def get_all(self):

        return []


    def create(self, data):

        return data


    def update(self, data):

        return data


    def delete(self, record_id):

        return record_id
