"""
AGS ERP V2
UI Component - App Entry
"""

import customtkinter as ctk


class AppEntry(ctk.CTkEntry):

    def __init__(
        self,
        parent,
        placeholder="",
        **kwargs
    ):

        super().__init__(
            parent,
            placeholder_text=placeholder,
            **kwargs
        )
