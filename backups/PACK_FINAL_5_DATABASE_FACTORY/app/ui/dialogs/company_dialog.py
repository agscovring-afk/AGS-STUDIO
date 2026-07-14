"""
AGS ERP V2
Company Dialog Extended
"""

import customtkinter as ctk

from app.models.company import Company


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


        self.title("Add Company")
        self.geometry("500x700")


        self.entries = {}


        fields = [
            "name",
            "commercial_name",
            "rc",
            "nif",
            "nis",
            "ai",
            "vat",
            "phone",
            "email",
            "website",
            "address",
            "bank",
            "rib",
            "iban",
            "swift"
        ]


        for field in fields:

            ctk.CTkLabel(
                self,
                text=field.upper()
            ).pack()


            entry = ctk.CTkEntry(
                self
            )

            entry.pack(
                pady=3
            )

            self.entries[field] = entry



        ctk.CTkButton(
            self,
            text="Save",
            command=self.save
        ).pack(
            pady=20
        )


        self.grab_set()



    def save(self):

        company = Company(
            name=self.entries["name"].get(),
            commercial_name=self.entries["commercial_name"].get(),
            rc=self.entries["rc"].get(),
            nif=self.entries["nif"].get(),
            nis=self.entries["nis"].get(),
            ai=self.entries["ai"].get(),
            vat=self.entries["vat"].get(),
            phone=self.entries["phone"].get(),
            email=self.entries["email"].get(),
            website=self.entries["website"].get(),
            address=self.entries["address"].get(),
            bank=self.entries["bank"].get(),
            rib=self.entries["rib"].get(),
            iban=self.entries["iban"].get(),
            swift=self.entries["swift"].get()
        )


        self.controller.create_company(
            company
        )


        self.refresh_callback()

        self.destroy()
