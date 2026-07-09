from generated.inventory.services.inventory_service import InventoryService

service = InventoryService()


def create(data):

    return service.create(data)


def get(id):

    return service.get(id)


def list_all():

    return service.list()


def update(id,data):

    return service.update(id,data)


def delete(id):

    return service.delete(id)
