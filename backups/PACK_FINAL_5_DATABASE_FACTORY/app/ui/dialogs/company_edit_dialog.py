"""
AGS ERP V2
Company Edit Dialog
"""

import customtkinter as ctk


class CompanyEditDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        controller,
        company,
        refresh_callback
    ):

        super().__init__(parent)

        self.controller = controller
        self.company = company
        self.refresh_callback = refresh_callback


        self.title("Edit Company")
        self.geometry("450x400")


        self.name = ctk.CTkEntry(self)
        self.name.pack(pady=10)

        self.name.insert(
            0,
            company["name"]
        )


        self.phone = ctk.CTkEntry(self)
        self.phone.pack(pady=10)

        self.phone.insert(
            0,
            company["phone"] or ""
        )


        self.email = ctk.CTkEntry(self)
        self.email.pack(pady=10)

        self.email.insert(
            0,
            company["email"] or ""
        )


        self.save = ctk.CTkButton(
            self,
            text="Save",
            command=self.update
        )

        self.save.pack(
            pady=20
        )


        self.grab_set()


    def update(self):

        self.company["name"] = self.name.get()
        self.company["phone"] = self.phone.get()
        self.company["email"] = self.email.get()


        self.controller.update_company(
            self.company
        )


        self.refresh_callback()

        self.destroy()
