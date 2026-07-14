
import tkinter as tk
from tkinter import ttk


from app.ai.crud_generator.crud_binding import bind_crud
from app.controllers.suppliers_payments_controller import SuppliersPaymentsController



class SuppliersPaymentsPage(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)


        self.controller = SuppliersPaymentsController()


        title = tk.Label(
            self,
            text="suppliers_payments Management"
        )

        title.pack()


        # =====================
        # TABLE
        # =====================

        self.table = ttk.Treeview(
            self
        )

        self.table.pack(
            fill="both",
            expand=True
        )


        # =====================
        # BUTTONS
        # =====================

        toolbar = tk.Frame(self)

        toolbar.pack()


        self.add_btn = tk.Button(
            toolbar,
            text="Add"
        )

        self.add_btn.pack(
            side="left"
        )


        self.edit_btn = tk.Button(
            toolbar,
            text="Edit"
        )

        self.edit_btn.pack(
            side="left"
        )


        self.delete_btn = tk.Button(
            toolbar,
            text="Delete"
        )

        self.delete_btn.pack(
            side="left"
        )


        bind_crud(
            self,
            self.controller
        )


    # =====================
    # CRUD DATA
    # =====================

    def get_form_data(self):

        return {}



    def get_selected_id(self):

        selected = self.table.selection()

        if selected:

            return self.table.item(
                selected[0]
            )["values"][0]

        return None
