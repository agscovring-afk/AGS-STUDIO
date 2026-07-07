"""
AGS ERP V2
Base Repository
"""

from app.database.database import Database


class BaseRepository:

    table_name = ""

    def __init__(self, db_path=None):
        self.db = Database(db_path)

    def connection(self):
        return self.db.connect()

    def execute(self, query, params=()):
        with self.connection() as conn:
            cur = conn.execute(query, params)
            conn.commit()
            return cur

    def fetchone(self, query, params=()):
        with self.connection() as conn:
            return conn.execute(query, params).fetchone()

    def fetchall(self, query, params=()):
        with self.connection() as conn:
            return conn.execute(query, params).fetchall()

    def delete(self, record_id):

        query = f"DELETE FROM {self.table_name} WHERE id=?"

        self.execute(query, (record_id,))

    def count(self):

        row = self.fetchone(
            f"SELECT COUNT(*) total FROM {self.table_name}"
        )

        return row["total"]