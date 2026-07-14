import tkinter as tk
import json

from app.core.router import Router


class MainWindow(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        Router.load_registry()

        self.pack(
            fill="both",
            expand=True
        )

        self.sidebar = tk.Frame(self)

        self.sidebar.pack(
            side="left",
            fill="y"
        )


        self.content = tk.Frame(self)

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )


        self.load_menu()



    def load_menu(self):

        with open(
            "app/registry/menu.json",
            "r",
            encoding="utf-8"
        ) as f:

            menu = json.load(f)


        for item in menu:

            btn = tk.Button(
                self.sidebar,
                text=item["name"],
                command=lambda r=item["route"]: self.open_page(r)
            )

            btn.pack(
                fill="x"
            )



    def open_page(self, route):

        for widget in self.content.winfo_children():

            widget.destroy()


        page = Router.load(
            route,
            self.content
        )


        if page and hasattr(page, "pack"):

            page.pack(
                fill="both",
                expand=True
            )