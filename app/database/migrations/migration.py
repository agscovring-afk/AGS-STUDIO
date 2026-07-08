import json
import os

from app.database.database import get_connection


METADATA = "app/metadata/modules"


def load_metadata(name):

    path = os.path.join(
        METADATA,
        f"{name}.json"
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def create_table(name):

    metadata = load_metadata(name)

    fields = metadata.get(
        "fields",
        []
    )


    conn = get_connection()
    cursor = conn.cursor()


    # Check table exists

    cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'"
    )

    exists = cursor.fetchone()


    if not exists:

        columns = []

        for field in fields:

            fname = field["name"]
            ftype = field["type"]


            if field.get("primary_key"):

                columns.append(
                    f"{fname} INTEGER PRIMARY KEY AUTOINCREMENT"
                )

            else:

                columns.append(
                    f"{fname} {ftype}"
                )


        query = f"""
        CREATE TABLE {name}
        (
            {','.join(columns)}
        )
        """

        cursor.execute(query)

        print(
            f"[DATABASE] Table created: {name}"
        )


    else:

        # Auto schema upgrade

        cursor.execute(
            f"PRAGMA table_info({name})"
        )

        existing = [
            row[1]
            for row in cursor.fetchall()
        ]


        for field in fields:

            fname = field["name"]
            ftype = field["type"]


            if fname not in existing:

                cursor.execute(
                    f"ALTER TABLE {name} ADD COLUMN {fname} {ftype}"
                )

                print(
                    f"[DATABASE] Column added: {name}.{fname}"
                )


        print(
            f"[DATABASE] Schema checked: {name}"
        )


    conn.commit()
    conn.close()