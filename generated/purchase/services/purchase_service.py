from generated.purchase.models.purchase import Purchase


class PurchaseService:


    def create(self,data):

        return Purchase(**data)


    def get(self,id):

        pass


    def list(self):

        return []


    def update(self,id,data):

        pass


    def delete(self,id):

        pass
