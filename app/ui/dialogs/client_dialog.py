"""
AGS ERP V2
Client Dialog
"""

import customtkinter as ctk


class ClientDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        save_callback
    ):

        super().__init__(
            parent
        )


        self.save_callback = save_callback


        self.title(
            "Add Client"
        )

        self.geometry(
            "500x500"
        )


        self.name = ctk.CTkEntry(
            self,
            placeholder_text="Client Name"
        )

        self.name.pack(
            pady=10
        )


        self.phone = ctk.CTkEntry(
            self,
            placeholder_text="Phone"
        )

        self.phone.pack(
            pady=10
        )


        button = ctk.CTkButton(
            self,
            text="Save",
            command=self.save
        )

        button.pack(
            pady=20
        )


    def save(self):

        data = {

            "name": self.name.get(),

            "phone": self.phone.get()

        }


        self.save_callback(
            data
        )

        self.destroy()
