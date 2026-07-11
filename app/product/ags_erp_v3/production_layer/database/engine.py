import sqlite3


class ProductionDatabase:

    def connect(self):

        self.db = sqlite3.connect(
            "ags_erp_v3.db"
        )

        return "DATABASE CONNECTED"


    def migrate(self):

        self.db.execute(
            "CREATE TABLE IF NOT EXISTS customers(id INTEGER PRIMARY KEY,name TEXT)"
        )

        self.db.commit()

        return "DATABASE MIGRATION READY"
