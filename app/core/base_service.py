"""
AGS ERP V2
Base Service
"""


class BaseService:

    def __init__(self, repository):
        self.repository = repository

    def create(self, *args, **kwargs):
        return self.repository.add(*args, **kwargs)

    def get(self, record_id):
        return self.repository.get(record_id)

    def all(self):
        return self.repository.list_all()

    def update(self, *args, **kwargs):
        return self.repository.update(*args, **kwargs)

    def delete(self, record_id):
        return self.repository.delete(record_id)

    def count(self):
        return self.repository.count()