"""
AGS ERP V2
Base Controller
"""


class BaseController:

    def __init__(self, service):
        self.service = service

    def create(self, *args, **kwargs):
        return self.service.create(*args, **kwargs)

    def get(self, record_id):
        return self.service.get(record_id)

    def list(self):
        return self.service.all()

    def update(self, *args, **kwargs):
        return self.service.update(*args, **kwargs)

    def delete(self, record_id):
        return self.service.delete(record_id)

    def count(self):
        return self.service.count()