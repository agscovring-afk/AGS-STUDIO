from generated.supplier.models.supplier import Supplier


class SupplierService:


    def create(self,data):

        return Supplier(**data)


    def get(self,id):

        pass


    def list(self):

        return []


    def update(self,id,data):

        pass


    def delete(self,id):

        pass
