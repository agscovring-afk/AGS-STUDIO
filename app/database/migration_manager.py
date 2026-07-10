"""
AGS ERP V2
Migration Manager
"""

import os
from app.database.database import get_connection


class MigrationManager:

    MIGRATION_PATH = "app/database/migrations"

    def __init__(self):
        self.connection = get_connection()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def applied_migrations(self):
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT name FROM migrations"
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]

    def get_files(self):
        if not os.path.exists(self.MIGRATION_PATH):
            return []

        return sorted(
            [
                f for f in os.listdir(self.MIGRATION_PATH)
                if f.endswith(".py")
            ]
        )

    def mark_applied(self, name):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO migrations(name)
            VALUES (?)
            """,
            (name,)
        )

        self.connection.commit()