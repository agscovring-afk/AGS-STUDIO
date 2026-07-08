def class_name(name):

    return ''.join(
        word.capitalize()
        for word in name.split('_')
    )


PAGE_TEMPLATE = '''
import tkinter as tk
from tkinter import ttk

from app.ai.crud_generator.crud_binding import bind_crud
from app.controllers.{module}_controller import {class_name}Controller
from app.ui.dialogs.{module}_dialog import {class_name}Dialog


class {class_name}Page(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.controller = {class_name}Controller()

        self.dialog_class = {class_name}Dialog


        title = tk.Label(
            self,
            text="{module} Management",
            font=("Arial", 14, "bold")
        )

        title.pack(
            pady=10
        )


        toolbar = tk.Frame(self)

        toolbar.pack(
            fill="x",
            padx=10,
            pady=5
        )


        self.add_btn = tk.Button(
            toolbar,
            text="Add",
            width=12
        )

        self.add_btn.pack(
            side="left",
            padx=5
        )


        self.edit_btn = tk.Button(
            toolbar,
            text="Edit",
            width=12
        )

        self.edit_btn.pack(
            side="left",
            padx=5
        )


        self.delete_btn = tk.Button(
            toolbar,
            text="Delete",
            width=12
        )

        self.delete_btn.pack(
            side="left",
            padx=5
        )


        self.table = ttk.Treeview(
            self
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        bind_crud(
            self,
            self.controller
        )


    def get_form_data(self):

        return {{}}


    def get_selected_id(self):

        selected = self.table.selection()

        if selected:

            return self.table.item(
                selected[0]
            )["values"][0]

        return None
'''


DIALOG_TEMPLATE = '''
import tkinter as tk


class {class_name}Dialog(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("{module} Dialog")

        self.geometry("300x150")

        self.data = {{}}


        tk.Label(
            self,
            text="Name"
        ).pack(
            pady=5
        )


        self.entry = tk.Entry(
            self,
            width=30
        )

        self.entry.pack(
            pady=5
        )


        tk.Button(
            self,
            text="Save",
            command=self.save
        ).pack(
            pady=10
        )


    def save(self):

        self.data = {{
            "name": self.entry.get()
        }}

        self.destroy()


    def get_data(self):

        return self.data
'''