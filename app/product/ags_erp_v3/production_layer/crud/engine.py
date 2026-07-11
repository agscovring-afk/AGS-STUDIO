class CRUDController:

    def create(self, data):
        return {"status":"created","data":data}

    def read(self, data):
        return {"status":"read","data":data}

    def update(self, data):
        return {"status":"updated","data":data}

    def delete(self, data):
        return {"status":"deleted","data":data}
