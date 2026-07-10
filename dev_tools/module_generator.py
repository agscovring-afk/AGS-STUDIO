"""
AGS ERP V2
Module Factory V3
CRUD Generator
"""

import sys
from pathlib import Path


def pascal(name):
    return name.replace("_", " ").title().replace(" ", "")


def write(path, content):

    file = Path(path)

    file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    file.write_text(
        content,
        encoding="utf-8"
    )


def generate(module):

    cls = pascal(module)
    table = module.lower() + "s"


    files = {


f"app/database/migrations/create_{table}.py":

f'''
def upgrade(conn):

    conn.execute("""
    CREATE TABLE IF NOT EXISTS {table} (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id INTEGER,

        code TEXT UNIQUE NOT NULL,

        name TEXT NOT NULL,

        status TEXT DEFAULT 'active',

        is_active INTEGER DEFAULT 1,

        created_at TEXT,

        updated_at TEXT

    )
    """)
''',



f"app/models/{module}.py":

f'''
class {cls}:


    def __init__(self, name):

        self.id = None
        self.company_id = None
        self.code = None
        self.name = name
        self.status = "active"
        self.is_active = 1
        self.created_at = None
        self.updated_at = None
''',



f"app/repositories/{module}_repository.py":

f'''
from app.core.base_repository import BaseRepository


class {cls}Repository(BaseRepository):


    table_name = "{table}"


    def create(self, obj):

        return self.execute(
            """
            INSERT INTO {table}
            (code,name,status,is_active)
            VALUES (?,?,?,?)
            """,
            (
                obj.code,
                obj.name,
                obj.status,
                obj.is_active
            )
        )


    def get_by_id(self,id):

        return self.fetchone(
            "SELECT * FROM {table} WHERE id=?",
            (id,)
        )


    def list_all(self):

        return self.fetchall(
            "SELECT * FROM {table}"
        )


    def delete(self,id):

        return self.execute(
            "UPDATE {table} SET is_active=0 WHERE id=?",
            (id,)
        )
''',



f"app/services/{module}_service.py":

f'''
class {cls}Service:


    def __init__(self, repository):

        self.repository = repository


    def create(self,obj):

        return self.repository.create(obj)


    def list_all(self):

        return self.repository.list_all()
''',



f"app/controllers/{module}_controller.py":

f'''
class {cls}Controller:


    def __init__(self,service):

        self.service = service


    def create(self,obj):

        return self.service.create(obj)


    def list(self):

        return self.service.list_all()
''',



f"app/ui/pages/{table}_page.py":

f'''
import customtkinter as ctk


class {cls}Page(ctk.CTkFrame):


    def __init__(self,parent):

        super().__init__(parent)


        ctk.CTkLabel(
            self,
            text="{cls}"
        ).pack()
''',



f"app/ui/dialogs/{module}_dialog.py":

f'''
import customtkinter as ctk


class {cls}Dialog(ctk.CTkToplevel):


    def __init__(self,parent):

        super().__init__(parent)

        self.title(
            "Add {cls}"
        )
''',



f"tests/test_{module}.py":

f'''
def test_{module}_crud():

    assert True
'''
    }


    for path,content in files.items():

        write(path,content)


    print(
        f"{cls} V3 module generated"
    )



if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "Usage: python module_generator.py module"
        )

        exit()


    generate(sys.argv[1])
