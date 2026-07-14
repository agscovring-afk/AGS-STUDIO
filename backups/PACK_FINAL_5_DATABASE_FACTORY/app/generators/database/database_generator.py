from pathlib import Path


class DatabaseGenerator:

    def generate(self,module):

        module=module.lower()

        path=Path("generated")/module/"database"

        path.mkdir(parents=True,exist_ok=True)

        sql=f'''
CREATE TABLE IF NOT EXISTS {module} (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    code TEXT NOT NULL UNIQUE,

    name TEXT NOT NULL,

    description TEXT,

    active BOOLEAN DEFAULT 1,

    created_at TIMESTAMP,

    updated_at TIMESTAMP

);

CREATE INDEX idx_{module}_code
ON {module}(code);

CREATE INDEX idx_{module}_name
ON {module}(name);
'''

        file=path/"migration.sql"

        file.write_text(
            sql,
            encoding="utf8"
        )

        return {

            "generator":"DatabaseGenerator",

            "status":"success",

            "file":str(file)

        }
