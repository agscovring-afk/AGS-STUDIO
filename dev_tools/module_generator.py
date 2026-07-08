"""
AGS ERP V2
Module Generator
"""

import sys
from pathlib import Path


BASE = Path(".")



TEMPLATES = {


"model.py":
'''
class {name_class}:

    def __init__(self, name):

        self.code = None
        self.name = name
        self.company_id = None
''',



"repository.py":
'''
from app.core.base_repository import BaseRepository


class {name_class}Repository(BaseRepository):

    table_name = "{name}"


    def list_all(self):

        return self.fetchall(
            "SELECT * FROM {name}"
        )
''',



"service.py":
'''
from app.core.base_service import BaseService


class {name_class}Service(BaseService):

    pass
''',



"controller.py":
'''
from app.core.base_controller import BaseController


class {name_class}Controller(BaseController):

    pass
''',



"page.py":
'''
import customtkinter as ctk


class {name_class}sPage(ctk.CTkFrame):

    def __init__(self,parent):

        super().__init__(parent)


        label = ctk.CTkLabel(
            self,
            text="{name_class}s"
        )

        label.pack()
''',



"dialog.py":
'''
import customtkinter as ctk


class {name_class}Dialog(ctk.CTkToplevel):

    def __init__(self,parent):

        super().__init__(parent)

        self.title(
            "Add {name_class}"
        )
'''

}



def create_module(name):

    name_lower = name.lower()

    name_class = name_lower.capitalize()


    paths = {

        "model.py":
        f"app/models/{name_lower}.py",

        "repository.py":
        f"app/repositories/{name_lower}_repository.py",

        "service.py":
        f"app/services/{name_lower}_service.py",

        "controller.py":
        f"app/controllers/{name_lower}_controller.py",

        "page.py":
        f"app/ui/pages/{name_lower}s_page.py",

        "dialog.py":
        f"app/ui/dialogs/{name_lower}_dialog.py"
    }



    for template,path in paths.items():

        file = Path(path)

        file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        content = TEMPLATES[template].format(
            name=name_lower,
            name_class=name_class
        )


        file.write_text(
            content,
            encoding="utf-8"
        )


    print(
        f"Module created: {name_class}"
    )



if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Usage: python module_generator.py module_name"
        )

        exit()


    create_module(
        sys.argv[1]
    )
