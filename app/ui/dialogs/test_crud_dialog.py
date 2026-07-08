
import tkinter as tk


class TestCrudDialog(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("test_crud Dialog")

        self.geometry("300x150")

        self.data = {}


        tk.Label(
            self,
            text="Name"
        ).pack(
            pady=5
        )


        self.entry = tk.Entry(
            self,
            width=30
        )

        self.entry.pack(
            pady=5
        )


        tk.Button(
            self,
            text="Save",
            command=self.save
        ).pack(
            pady=10
        )


    def save(self):

        self.data = {
            "name": self.entry.get()
        }

        self.destroy()


    def get_data(self):

        return self.data
