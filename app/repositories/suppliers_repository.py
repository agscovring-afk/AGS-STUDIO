
from app.models.suppliers import Suppliers


class SuppliersRepository:

    model = Suppliers


    def get_all(self):

        return []


    def create(self, data):

        return data


    def update(self, data):

        return data


    def delete(self, record_id):

        return record_id
