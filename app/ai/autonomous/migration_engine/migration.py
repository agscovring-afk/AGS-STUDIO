from ..engine_base import EngineBase
from ..workers.bridge import bridge


class MigrationEngine(EngineBase):

    name = "MIGRATION_ENGINE_V1"


    def run(self, context):

        if isinstance(context, str):
            module = context.replace("CREATE ERP MODULE", "").strip().lower().replace(" ", "_")
        else:
            module = context.get("module", "module")

        migration = f'''-- AGS Migration V1

CREATE TABLE IF NOT EXISTS {module} (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

'''

        result = bridge.dispatch(
            "file_creator",
            {
                "files": [
                    {
                        "path": f"generated/modules/{module}/migrations/0001_initial.sql",
                        "content": migration
                    }
                ]
            }
        )

        return {
            "engine": self.name,
            "status": "completed",
            "module": module,
            "result": result
        }
