"""
AGS ERP V2
UI Component - App Button
"""

import customtkinter as ctk


class AppButton(ctk.CTkButton):

    def __init__(
        self,
        parent,
        text,
        command=None,
        **kwargs
    ):

        super().__init__(
            parent,
            text=text,
            command=command,
            **kwargs
        )
