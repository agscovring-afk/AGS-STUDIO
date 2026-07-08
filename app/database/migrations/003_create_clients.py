"""
AGS ERP V2
Migration 003 - Create Clients Table
"""

from app.database.database import Database


def run():

    db = Database()

    with db.connect() as conn:

        conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            company_id INTEGER,

            code TEXT UNIQUE NOT NULL,

            name TEXT NOT NULL,

            contact TEXT,
            function TEXT,

            phone TEXT,
            mobile TEXT,

            email TEXT,

            address TEXT,
            city TEXT,
            wilaya TEXT,
            country TEXT,

            rc TEXT,
            nif TEXT,
            nis TEXT,
            ai TEXT,

            bank TEXT,
            rib TEXT,

            status TEXT DEFAULT 'active',

            is_active INTEGER DEFAULT 1,

            created_at TEXT,
            updated_at TEXT
        )
        """)


if __name__ == "__main__":
    run()
