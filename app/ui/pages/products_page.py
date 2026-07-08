
import tkinter as tk


class ProductsPage(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)


        title = tk.Label(
            self,
            text="products Management"
        )

        title.pack()
