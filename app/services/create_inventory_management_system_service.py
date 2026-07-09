
from app.repositories.create_inventory_management_system_repository import CreateInventoryManagementSystemRepository


class CreateInventoryManagementSystemService:

    repository = CreateInventoryManagementSystemRepository()


    def get_all(self):

        return self.repository.get_all()


    def create(self, data):

        return self.repository.create(data)


    def update(self, data):

        return self.repository.update(data)


    def delete(self, record_id):

        return self.repository.delete(record_id)
