from app.repositories.base_repository import BaseRepository


class EmployeeRepository(BaseRepository):

    def __init__(self, db_path=None):
        super().__init__(db_path)
