"""
AGS ERP V2
Reusable Table Component
"""

import customtkinter as ctk


class AppTable(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        columns
    ):

        super().__init__(
            parent
        )

        self.columns = columns

        self.rows = []


        self.header = ctk.CTkFrame(
            self
        )

        self.header.pack(
            fill="x"
        )


        for col in columns:

            label = ctk.CTkLabel(
                self.header,
                text=col,
                width=120
            )

            label.pack(
                side="left",
                padx=2
            )


        self.body = ctk.CTkScrollableFrame(
            self
        )

        self.body.pack(
            fill="both",
            expand=True
        )


    def load_data(
        self,
        data
    ):

        for widget in self.body.winfo_children():

            widget.destroy()


        for row in data:

            frame = ctk.CTkFrame(
                self.body
            )

            frame.pack(
                fill="x",
                pady=2
            )


            for col in self.columns:

                value = row[col.lower()] if col.lower() in row.keys() else ""

                label = ctk.CTkLabel(
                    frame,
                    text=str(value),
                    width=120
                )

                label.pack(
                    side="left",
                    padx=2
                )
