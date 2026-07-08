import json
import os


class SchemaEngine:

    METADATA = "app/metadata/modules"


    @classmethod
    def load(cls, module):

        path = os.path.join(
            cls.METADATA,
            f"{module}.json"
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    @classmethod
    def create_sql(cls, module):

        metadata = cls.load(module)

        columns = []

        for field in metadata["fields"]:

            sql = f'{field["name"]} {field["type"]}'

            if field.get("primary_key"):

                sql += " PRIMARY KEY"

            if field.get("nullable") is False:

                sql += " NOT NULL"

            columns.append(sql)

        query = f'''
CREATE TABLE IF NOT EXISTS {metadata["table"]} (
    {", ".join(columns)}
);
'''

        return query