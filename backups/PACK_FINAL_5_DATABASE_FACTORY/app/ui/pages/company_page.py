"""
AGS ERP V2
Company Page
"""

import customtkinter as ctk

from app.ui.dialogs.company_dialog import CompanyDialog
from app.ui.dialogs.company_edit_dialog import CompanyEditDialog


class CompanyPage(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        controller
    ):

        super().__init__(parent)

        self.controller = controller
        self.selected_company = None


        ctk.CTkLabel(
            self,
            text="Companies",
            font=("Arial",24)
        ).pack(pady=20)


        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=20)


        ctk.CTkButton(
            toolbar,
            text="Add",
            command=self.add
        ).pack(side="left", padx=5)


        ctk.CTkButton(
            toolbar,
            text="Edit",
            command=self.edit
        ).pack(side="left", padx=5)


        ctk.CTkButton(
            toolbar,
            text="Deactivate",
            command=self.deactivate
        ).pack(side="left", padx=5)


        self.table = ctk.CTkTextbox(
            self
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        self.table.bind(
            "<ButtonRelease-1>",
            self.select
        )


        self.load_data()



    def load_data(self):

        self.table.delete(
            "1.0",
            "end"
        )


        self.companies = self.controller.get_companies()


        for c in self.companies:

            self.table.insert(
                "end",
                f"{c['id']} | {c['code']} | {c['name']}\n"
            )


    def select(self,event=None):

        line = self.table.index(
            "insert"
        )

        index = int(
            line.split(".")[0]
        ) - 1


        if index >= 0 and index < len(self.companies):

            self.selected_company = self.companies[index]



    def add(self):

        CompanyDialog(
            self,
            self.controller,
            self.load_data
        )



    def edit(self):

        if self.selected_company:

            CompanyEditDialog(
                self,
                self.controller,
                self.selected_company,
                self.load_data
            )



    def deactivate(self):

        if self.selected_company:

            self.controller.deactivate(
                self.selected_company["id"]
            )

            self.load_data()
