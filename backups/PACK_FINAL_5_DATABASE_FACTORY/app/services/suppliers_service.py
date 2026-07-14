
from app.repositories.suppliers_repository import SuppliersRepository


class SuppliersService:

    repository = SuppliersRepository()


    def get_all(self):

        return self.repository.get_all()


    def create(self, data):

        return self.repository.create(data)


    def update(self, data):

        return self.repository.update(data)


    def delete(self, record_id):

        return self.repository.delete(record_id)
