def class_name(name):

    return ''.join(
        word.capitalize()
        for word in name.split('_')
    )


PAGE_TEMPLATE = '''
import tkinter as tk
from tkinter import ttk


class {class_name}Page(tk.Frame):

    def __init__(self, parent, controller=None):

        super().__init__(parent)

        self.controller = controller


        title = tk.Label(
            self,
            text="{module} Management",
            font=("Arial", 16)
        )

        title.pack(pady=10)


        self.search = tk.Entry(self)

        self.search.pack(
            fill="x",
            padx=20
        )


        columns = (
            "id",
            "name"
        )


        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )


        for col in columns:

            self.table.heading(
                col,
                text=col.upper()
            )


        self.table.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=10
        )


        buttons = tk.Frame(self)

        buttons.pack()


        tk.Button(
            buttons,
            text="Add"
        ).pack(
            side="left",
            padx=5
        )


        tk.Button(
            buttons,
            text="Edit"
        ).pack(
            side="left",
            padx=5
        )


        tk.Button(
            buttons,
            text="Delete"
        ).pack(
            side="left",
            padx=5
        )
'''



DIALOG_TEMPLATE = '''
import tkinter as tk


class {class_name}Dialog(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)


        self.title(
            "{module} Form"
        )


        tk.Label(
            self,
            text="{module} Name"
        ).pack()


        self.entry = tk.Entry(self)

        self.entry.pack()


        tk.Button(
            self,
            text="Save"
        ).pack()
'''
