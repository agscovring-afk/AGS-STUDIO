"""
AGS ERP V2
UI Component - App Table
"""

import customtkinter as ctk


class AppTable(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        columns,
        **kwargs
    ):

        super().__init__(
            parent,
            **kwargs
        )

        self.columns = columns

        self.table = ctk.CTkTextbox(
            self
        )

        self.table.pack(
            fill="both",
            expand=True
        )


    def clear(self):

        self.table.delete(
            "0.0",
            "end"
        )


    def insert_row(self, values):

        row = " | ".join(
            str(v) for v in values
        )

        self.table.insert(
            "end",
            row + "\n"
        )
