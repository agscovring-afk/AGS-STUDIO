from app.database.database import get_connection


class BaseModel:

    table_name = None

    @classmethod
    def execute(cls, query, params=()):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor

    def save(self):
        pass
