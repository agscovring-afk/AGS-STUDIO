"""
AGS ERP V2
Company Page
"""

import customtkinter as ctk


class CompanyPage(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        controller
    ):

        super().__init__(parent)

        self.controller = controller


        self.title = ctk.CTkLabel(
            self,
            text="Companies",
            font=("Arial", 24)
        )

        self.title.pack(
            pady=20
        )


        self.refresh_button = ctk.CTkButton(
            self,
            text="Refresh",
            command=self.load_data
        )

        self.refresh_button.pack(
            pady=5
        )


        self.table = ctk.CTkTextbox(
            self,
            font=("Consolas", 14)
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        self.load_data()


    def load_data(self):

        self.table.delete(
            "1.0",
            "end"
        )


        companies = self.controller.get_companies()


        for company in companies:

            self.table.insert(
                "end",
                f"""
Code: {company['code']}
Name: {company['name']}
Commercial: {company['commercial_name']}
Phone: {company['phone']}
-----------------------------
"""
            )
