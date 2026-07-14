import json
import os


class MetadataEngine:

    BASE = "app/metadata/modules"


    @classmethod
    def ensure(cls):
        os.makedirs(
            cls.BASE,
            exist_ok=True
        )


    @classmethod
    def create(cls, module, fields=None):

        cls.ensure()


        if fields is None:

            fields = [
                {
                    "name": "id",
                    "type": "INTEGER",
                    "primary_key": True
                },
                {
                    "name": "name",
                    "type": "TEXT"
                }
            ]


        data = {

            "module": module,

            "table": module,

            "fields": fields

        }


        path = os.path.join(
            cls.BASE,
            f"{module}.json"
        )


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )


        print(
            f"[METADATA] Created: {path}"
        )