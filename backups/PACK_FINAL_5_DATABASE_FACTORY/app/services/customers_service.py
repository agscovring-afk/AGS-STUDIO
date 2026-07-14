
from app.repositories.customers_repository import CustomersRepository


class CustomersService:

    repository = CustomersRepository()


    def get_all(self):

        return self.repository.get_all()


    def create(self, data):

        return self.repository.create(data)


    def update(self, data):

        return self.repository.update(data)


    def delete(self, record_id):

        return self.repository.delete(record_id)
