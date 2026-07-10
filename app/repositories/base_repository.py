from app.database.database import Database


class BaseRepository:
    def __init__(self, db_path=None):
        self.db = Database(db_path)

    def connection(self):
        return self.db.connect()