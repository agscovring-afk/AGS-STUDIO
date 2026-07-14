
import tkinter as tk


class OrdersDialog(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)


        self.title(
            "orders Form"
        )


        tk.Label(
            self,
            text="orders Name"
        ).pack()


        self.entry = tk.Entry(self)

        self.entry.pack()


        tk.Button(
            self,
            text="Save"
        ).pack()
