"""
AGS ERP V2
Client Repository
"""

from app.core.base_repository import BaseRepository


class ClientRepository(BaseRepository):

    table_name = "clients"


    def create(self, client):

        query = """
        INSERT INTO clients
        (
            code,
            name,
            contact,
            function,
            phone,
            mobile,
            email,
            address,
            city,
            wilaya,
            country,
            rc,
            nif,
            nis,
            ai,
            bank,
            rib,
            company_id,
            status,
            is_active,
            created_at,
            updated_at
        )

        VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """


        params = (

            client.code,
            client.name,
            client.contact,
            client.function,
            client.phone,
            client.mobile,
            client.email,
            client.address,
            client.city,
            client.wilaya,
            client.country,
            client.rc,
            client.nif,
            client.nis,
            client.ai,
            client.bank,
            client.rib,
            client.company_id,
            client.status,
            client.is_active,
            client.created_at,
            client.updated_at
        )


        return self.execute(
            query,
            params
        )


    def list_all(self):

        return self.fetchall(
            """
            SELECT *
            FROM clients
            WHERE is_active = 1
            ORDER BY id DESC
            """
        )


    def get_by_code(self, code):

        return self.fetchone(
            """
            SELECT *
            FROM clients
            WHERE code = ?
            """,
            (code,)
        )


    def deactivate(self, client_id):

        self.execute(
            """
            UPDATE clients
            SET is_active = 0
            WHERE id = ?
            """,
            (client_id,)
        )
