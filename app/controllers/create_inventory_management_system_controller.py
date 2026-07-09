
from app.services.create_inventory_management_system_service import CreateInventoryManagementSystemService


class CreateInventoryManagementSystemController:

    service = CreateInventoryManagementSystemService()


    def get_all(self):

        return self.service.get_all()


    def create(self, data):

        return self.service.create(data)


    def update(self, data):

        return self.service.update(data)


    def delete(self, record_id):

        return self.service.delete(record_id)
