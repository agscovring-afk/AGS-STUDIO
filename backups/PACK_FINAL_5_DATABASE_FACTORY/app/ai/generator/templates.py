def class_name(name):

    return ''.join(
        word.capitalize()
        for word in name.split('_')
    )


MODEL_TEMPLATE = '''
from app.models.base_model import BaseModel


class {class_name}(BaseModel):

    table_name = "{module}"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
'''


REPOSITORY_TEMPLATE = '''
from app.models.{module} import {class_name}


class {class_name}Repository:

    model = {class_name}


    def get_all(self):

        return []


    def create(self, data):

        return data


    def update(self, data):

        return data


    def delete(self, record_id):

        return record_id
'''


SERVICE_TEMPLATE = '''
from app.repositories.{module}_repository import {class_name}Repository


class {class_name}Service:

    repository = {class_name}Repository()


    def get_all(self):

        return self.repository.get_all()


    def create(self, data):

        return self.repository.create(data)


    def update(self, data):

        return self.repository.update(data)


    def delete(self, record_id):

        return self.repository.delete(record_id)
'''


CONTROLLER_TEMPLATE = '''
from app.services.{module}_service import {class_name}Service


class {class_name}Controller:

    service = {class_name}Service()


    def get_all(self):

        return self.service.get_all()


    def create(self, data):

        return self.service.create(data)


    def update(self, data):

        return self.service.update(data)


    def delete(self, record_id):

        return self.service.delete(record_id)
'''
