
from app.repositories.test_memory_repository import TestMemoryRepository


class TestMemoryService:

    repository = TestMemoryRepository()


    def get_all(self):

        return self.repository.get_all()


    def create(self, data):

        return self.repository.create(data)


    def update(self, data):

        return self.repository.update(data)


    def delete(self, record_id):

        return self.repository.delete(record_id)
