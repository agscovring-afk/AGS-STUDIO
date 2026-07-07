"""
AGS ERP V2
UI Component - App Card
"""

import customtkinter as ctk


class AppCard(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        title="",
        value="",
        **kwargs
    ):

        super().__init__(
            parent,
            **kwargs
        )


        self.title_label = ctk.CTkLabel(
            self,
            text=title
        )

        self.title_label.pack(
            pady=5
        )


        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Arial", 24)
        )

        self.value_label.pack(
            pady=10
        )


    def update_value(
        self,
        value
    ):

        self.value_label.configure(
            text=value
        )
