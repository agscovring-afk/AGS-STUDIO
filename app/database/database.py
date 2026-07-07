
import sqlite3
from pathlib import Path

DB_NAME = "ags_erp.db"


class Database:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else Path.cwd() / DB_NAME

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn