"""
AGS ERP V2
Company Page
"""

import customtkinter as ctk

from app.ui.dialogs.company_dialog import CompanyDialog


class CompanyPage(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        controller
    ):

        super().__init__(parent)

        self.controller = controller
        self.selected_company = None


        self.title = ctk.CTkLabel(
            self,
            text="Companies",
            font=("Arial", 24)
        )

        self.title.pack(
            pady=20
        )


        self.toolbar = ctk.CTkFrame(self)

        self.toolbar.pack(
            fill="x",
            padx=20
        )


        self.add_button = ctk.CTkButton(
            self.toolbar,
            text="Add Company",
            command=self.open_add_dialog
        )

        self.add_button.pack(
            side="left",
            padx=5
        )


        self.refresh_button = ctk.CTkButton(
            self.toolbar,
            text="Refresh",
            command=self.load_data
        )

        self.refresh_button.pack(
            side="left",
            padx=5
        )


        self.table = ctk.CTkTextbox(
            self,
            font=("Consolas",14)
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        self.table.bind(
            "<ButtonRelease-1>",
            self.select_company
        )


        self.load_data()


    def open_add_dialog(self):

        CompanyDialog(
            self,
            self.controller,
            self.load_data
        )


    def select_company(self,event=None):

        self.selected_company = None


    def load_data(self):

        self.table.delete(
            "1.0",
            "end"
        )


        companies = self.controller.get_companies()


        for company in companies:

            self.table.insert(
                "end",
                f"{company['id']} | {company['code']} | {company['name']}\n"
            )
