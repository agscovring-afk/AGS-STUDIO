
import customtkinter as ctk


class SuppliersPage(ctk.CTkFrame):

    def __init__(self,parent):

        super().__init__(parent)


        label = ctk.CTkLabel(
            self,
            text="Suppliers"
        )

        label.pack()
