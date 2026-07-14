
import tkinter as tk

class FinancePage(tk.Frame):

    def __init__(self,parent):
        super().__init__(parent)

        tk.Label(
            self,
            text="Finance",
            font=("Arial",22)
        ).pack(pady=40)

        tk.Label(
            self,
            text="AGS Enterprise Autonomous Platform"
        ).pack()
