from datetime import datetime
from typing import Optional

from app.models.client import Client
from app.repositories.base_repository import BaseRepository


class ClientRepository(BaseRepository):

    def __init__(self, db_path=None):
        super().__init__(db_path)

    def create_table(self):
        with self.connection() as c:
            c.execute("""
            CREATE TABLE IF NOT EXISTS clients (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                company_id INTEGER,

                code TEXT UNIQUE,

                name TEXT NOT NULL,

                contact TEXT,
                contact_function TEXT,

                phone TEXT,
                mobile TEXT,

                email TEXT,

                address TEXT,
                city TEXT,
                wilaya TEXT,
                country TEXT,
                postal_code TEXT,

                rc TEXT,
                nif TEXT,
                nis TEXT,
                ai TEXT,

                bank TEXT,
                rib TEXT,

                notes TEXT,

                status TEXT DEFAULT 'active',

                is_active INTEGER DEFAULT 1,

                created_at TEXT,

                updated_at TEXT

            )
            """)

    def add(self, client: Client) -> int:

        with self.connection() as c:

            cur = c.execute(
                """
                INSERT INTO clients(

                    company_id,
                    code,
                    name,
                    contact,
                    contact_function,
                    phone,
                    mobile,
                    email,
                    address,
                    city,
                    wilaya,
                    country,
                    postal_code,
                    rc,
                    nif,
                    nis,
                    ai,
                    bank,
                    rib,
                    notes,
                    status,
                    is_active,
                    created_at,
                    updated_at

                )

                VALUES(

                    ?,?,?,?,?,?,
                    ?,?,?,?,?,?,
                    ?,?,?,?,?,?,
                    ?,?,?,?,?,?

                )
                """,
                (
                    client.company_id,
                    client.code,
                    client.name,
                    client.contact,
                    client.contact_function,
                    client.phone,
                    client.mobile,
                    client.email,
                    client.address,
                    client.city,
                    client.wilaya,
                    client.country,
                    client.postal_code,
                    client.rc,
                    client.nif,
                    client.nis,
                    client.ai,
                    client.bank,
                    client.rib,
                    client.notes,
                    client.status,
                    1 if client.is_active else 0,
                    client.created_at.isoformat(),
                    client.updated_at.isoformat(),
                ),
            )

            return cur.lastrowid
            def get(self, client_id: int) -> Optional[Client]:

        with self.connection() as c:

            row = c.execute(
                "SELECT * FROM clients WHERE id=?",
                (client_id,),
            ).fetchone()

            if row is None:
                return None

            return Client(
                id=row["id"],
                company_id=row["company_id"],
                code=row["code"],
                name=row["name"],
                contact=row["contact"],
                contact_function=row["contact_function"],
                phone=row["phone"],
                mobile=row["mobile"],
                email=row["email"],
                address=row["address"],
                city=row["city"],
                wilaya=row["wilaya"],
                country=row["country"],
                postal_code=row["postal_code"],
                rc=row["rc"],
                nif=row["nif"],
                nis=row["nis"],
                ai=row["ai"],
                bank=row["bank"],
                rib=row["rib"],
                notes=row["notes"],
                status=row["status"],
                is_active=bool(row["is_active"]),
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
            )

    def list_all(self, include_inactive=False):

        with self.connection() as c:

            if include_inactive:
                rows = c.execute(
                    "SELECT * FROM clients ORDER BY id"
                ).fetchall()
            else:
                rows = c.execute(
                    "SELECT * FROM clients WHERE is_active=1 ORDER BY id"
                ).fetchall()

        return [self.get(r["id"]) for r in rows]