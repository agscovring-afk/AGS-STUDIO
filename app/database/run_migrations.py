"""
AGS ERP V2
Run Database Migrations
"""

import importlib

from app.database.database import get_connection
from app.database.migration_manager import MigrationManager


def main():

    connection = get_connection()

    manager = MigrationManager()

    manager.create_table()

    migration_name = "001_create_companies_table"

    applied = manager.applied_migrations()

    if migration_name not in applied:

        migration = importlib.import_module(
            "app.database.migrations.001_create_companies_table"
        )

        migration.upgrade(connection)

        manager.mark_applied(migration_name)

        print("Migration applied:", migration_name)

    else:

        print("Migration already applied")


if __name__ == "__main__":
    main()
