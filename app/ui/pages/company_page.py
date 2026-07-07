"""
AGS ERP V2
Company Page
"""

import customtkinter as ctk


class CompanyPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.title = ctk.CTkLabel(
            self,
            text="Companies",
            font=("Arial", 24)
        )

        self.title.pack(
            pady=20
        )


        self.toolbar = ctk.CTkFrame(
            self
        )

        self.toolbar.pack(
            fill="x",
            padx=20
        )


        self.add_button = ctk.CTkButton(
            self.toolbar,
            text="Add Company"
        )

        self.add_button.pack(
            side="left",
            padx=5
        )


        self.edit_button = ctk.CTkButton(
            self.toolbar,
            text="Edit"
        )

        self.edit_button.pack(
            side="left",
            padx=5
        )


        self.delete_button = ctk.CTkButton(
            self.toolbar,
            text="Deactivate"
        )

        self.delete_button.pack(
            side="left",
            padx=5
        )


        self.table = ctk.CTkTextbox(
            self
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        self.load_data()


    def load_data(self):

        self.table.insert(
            "end",
            "Company list will appear here..."
        )
