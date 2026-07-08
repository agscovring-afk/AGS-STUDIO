
from app.core.base_repository import BaseRepository


class SupplierRepository(BaseRepository):

    table_name = "supplier"


    def list_all(self):

        return self.fetchall(
            "SELECT * FROM supplier"
        )
