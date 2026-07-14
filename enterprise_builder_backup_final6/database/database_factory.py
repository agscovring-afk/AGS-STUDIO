from pathlib import Path

from .schema.schema_generator import SchemaGenerator
from .migrations.migration_generator import MigrationGenerator
from .generators.index_generator import IndexGenerator
from .generators.tenant_generator import TenantGenerator


class DatabaseFactory:
    """
    Enterprise Database Factory

    Metadata
        ↓
    Schema Generation
        ↓
    Migration Generation
        ↓
    Index Generation
        ↓
    Tenant Isolation
    """

    def __init__(self, workspace=None):
        self.workspace = Path(workspace or "workspace")

        self.schema_generator = SchemaGenerator(
            self.workspace
        )

        self.migration_generator = MigrationGenerator(
            self.workspace
        )

        self.index_generator = IndexGenerator(
            self.workspace
        )

        self.tenant_generator = TenantGenerator(
            self.workspace
        )


    def build(self, metadata):
        database_result = {
            "schema": None,
            "migrations": None,
            "indexes": None,
            "tenant": None
        }

        database_result["schema"] = (
            self.schema_generator.generate(metadata)
        )

        database_result["migrations"] = (
            self.migration_generator.generate(metadata)
        )

        database_result["indexes"] = (
            self.index_generator.generate(metadata)
        )

        database_result["tenant"] = (
            self.tenant_generator.generate(metadata)
        )

        return database_result
