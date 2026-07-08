"""
AGS ERP V2
Module Factory V2
"""

import sys
from pathlib import Path
from datetime import datetime


def class_name(name):

    return name.capitalize()



def write_file(path, content):

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

    cls = class_name(module)


    files = {


f"app/database/migrations/create_{module}.py":

f'''
"""
Migration: Create {module} table
"""

def upgrade(conn):

    conn.execute("""
    CREATE TABLE IF NOT EXISTS {module}s (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id INTEGER,

        code TEXT UNIQUE NOT NULL,

        name TEXT NOT NULL,

        is_active INTEGER DEFAULT 1,

        created_at TEXT,

        updated_at TEXT
    )
    """)
''',



f"app/models/{module}.py":

f'''
"""
{cls} Model
"""


class {cls}:


    def __init__(
        self,
        name
    ):

        self.id = None
        self.code = None
        self.name = name
        self.company_id = None
        self.is_active = 1
        self.created_at = None
        self.updated_at = None
''',



f"app/repositories/{module}_repository.py":

f'''
from app.core.base_repository import BaseRepository


class {cls}Repository(BaseRepository):


    table_name = "{module}s"



    def list_all(self):

        return self.fetchall(
            "SELECT * FROM {module}s WHERE is_active=1"
        )
''',



f"app/services/{module}_service.py":

f'''
from app.core.base_service import BaseService


class {cls}Service(BaseService):


    pass
''',



f"app/controllers/{module}_controller.py":

f'''
from app.core.base_controller import BaseController


class {cls}Controller(BaseController):


    pass
''',



f"app/ui/pages/{module}s_page.py":

f'''
import customtkinter as ctk



class {cls}sPage(ctk.CTkFrame):


    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent
        )


        title = ctk.CTkLabel(
            self,
            text="{cls}s"
        )


        title.pack(
            pady=20
        )
''',



f"app/ui/dialogs/{module}_dialog.py":

f'''
import customtkinter as ctk



class {cls}Dialog(ctk.CTkToplevel):


    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent
        )


        self.title(
            "Add {cls}"
        )
''',



f"tests/test_{module}.py":

f'''
"""
Test {cls} module
"""


def test_{module}_creation():

    assert True
'''
    }



    for path,content in files.items():

        write_file(
            path,
            content
        )


    print(
        f"{cls} module generated successfully"
    )



if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Usage: python module_generator.py module_name"
        )

        exit()


    generate(
        sys.argv[1]
    )
