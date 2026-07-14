
import tkinter as tk
from tkinter import ttk

from app.ai.crud_generator.crud_binding import bind_crud
from app.controllers.suppliers_controller import SuppliersController
from app.ui.dialogs.suppliers_dialog import SuppliersDialog


class SuppliersPage(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.controller = SuppliersController()

        self.dialog_class = SuppliersDialog


        title = tk.Label(
            self,
            text="suppliers Management",
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

        return {}


    def get_selected_id(self):

        selected = self.table.selection()

        if selected:

            return self.table.item(
                selected[0]
            )["values"][0]

        return None
