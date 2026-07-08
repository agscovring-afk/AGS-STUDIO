
import tkinter as tk


class SuppliersPage(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)


        title = tk.Label(
            self,
            text="suppliers Management"
        )

        title.pack()
