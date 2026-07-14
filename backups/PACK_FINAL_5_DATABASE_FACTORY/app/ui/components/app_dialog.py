"""
AGS ERP V2
UI Component - App Dialog
"""

import customtkinter as ctk


class AppDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        title="",
        width=400,
        height=300
    ):

        super().__init__(parent)

        self.title(title)

        self.geometry(
            f"{width}x{height}"
        )

        self.grab_set()
