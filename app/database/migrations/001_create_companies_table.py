"""
AGS ERP V2
Migration 001
Create Companies Table
"""


def upgrade(connection):

    query = """
    CREATE TABLE IF NOT EXISTS companies (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        code TEXT UNIQUE NOT NULL,

        name TEXT NOT NULL,
        commercial_name TEXT,

        phone TEXT,
        email TEXT,
        address TEXT,

        rc TEXT,
        nif TEXT,
        nis TEXT,
        ai TEXT,

        currency TEXT DEFAULT 'DZD',
        language TEXT DEFAULT 'fr',

        company_id INTEGER,

        is_active INTEGER DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
