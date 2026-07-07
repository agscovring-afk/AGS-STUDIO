"""
AGS ERP V2
UI Component - App Toolbar
"""

import customtkinter as ctk


class AppToolbar(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        **kwargs
    ):

        super().__init__(
            parent,
            **kwargs
        )


    def add_button(
        self,
        button
    ):

        button.pack(
            side="left",
            padx=5,
            pady=5
        )
