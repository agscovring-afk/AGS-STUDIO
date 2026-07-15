import json
import os


class MetadataEngine:

    BASE = "app/metadata/modules"


    TEMPLATES = {

        "customers": [
            ("name", "TEXT"),
            ("phone", "TEXT"),
            ("email", "TEXT"),
            ("address", "TEXT")
        ],


        "suppliers": [
            ("name", "TEXT"),
            ("phone", "TEXT"),
            ("email", "TEXT"),
            ("address", "TEXT")
        ],


        "products": [
            ("name", "TEXT"),
            ("reference", "TEXT"),
            ("price", "REAL"),
            ("quantity", "INTEGER")
        ],


        "invoices": [
            ("customer_id", "INTEGER"),
            ("date", "TEXT"),
            ("total", "REAL"),
            ("status", "TEXT")
        ],


        "orders": [
            ("customer_id", "INTEGER"),
            ("date", "TEXT"),
            ("total", "REAL")
        ]
    }



    @classmethod
    def ensure(cls):

        os.makedirs(
            cls.BASE,
            exist_ok=True
        )



    @classmethod
    def create(cls, module):

        cls.ensure()


        fields = [

            {
                "name": "id",
                "type": "INTEGER",
                "primary_key": True
            }

        ]


        template = cls.TEMPLATES.get(
            module,
            [
                ("name","TEXT")
            ]
        )


        for name, dtype in template:

            fields.append(
                {
                    "name": name,
                    "type": dtype
                }
            )


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