
import customtkinter as ctk


class SupplierDialog(ctk.CTkToplevel):

    def __init__(self,parent):

        super().__init__(parent)

        self.title(
            "Add Supplier"
        )
