"""
AGS ERP V2
Company Dialog
"""

import customtkinter as ctk


class CompanyDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        controller,
        refresh_callback
    ):

        super().__init__(parent)

        self.controller = controller
        self.refresh_callback = refresh_callback


        self.title(
            "Add Company"
        )

        self.geometry(
            "450x500"
        )


        self.entries = {}


        fields = [
            "name",
            "commercial_name",
            "phone",
            "email",
            "address"
        ]


        for field in fields:

            label = ctk.CTkLabel(
                self,
                text=field.capitalize()
            )

            label.pack(
                pady=5
            )


            entry = ctk.CTkEntry(
                self
            )

            entry.pack(
                padx=20
            )


            self.entries[field] = entry



        self.save_button = ctk.CTkButton(
            self,
            text="Save",
            command=self.save
        )

        self.save_button.pack(
            pady=20
        )


        self.grab_set()



    def save(self):

        from app.models.company import Company


        company = Company(
            name=self.entries["name"].get(),
            commercial_name=self.entries["commercial_name"].get(),
            phone=self.entries["phone"].get(),
            email=self.entries["email"].get(),
            address=self.entries["address"].get()
        )


        self.controller.create_company(
            company
        )


        self.refresh_callback()


        self.destroy()
