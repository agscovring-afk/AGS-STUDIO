"""
AGS ERP V2
Migration 002 - Extend Companies
"""

from app.database.database import Database


def run():

    db = Database()

    with db.connect() as conn:

        columns = [
            ("website", "TEXT"),
            ("bank", "TEXT"),
            ("rib", "TEXT"),
            ("iban", "TEXT"),
            ("swift", "TEXT"),
            ("vat", "TEXT"),
            ("logo", "TEXT")
        ]

        existing = [
            row["name"]
            for row in conn.execute(
                "PRAGMA table_info(companies)"
            )
        ]

        for name, dtype in columns:

            if name not in existing:

                conn.execute(
                    f"ALTER TABLE companies ADD COLUMN {name} {dtype}"
                )


if __name__ == "__main__":
    run()
