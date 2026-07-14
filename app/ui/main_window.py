
import tkinter as tk
from app.core.router import Router


class MainWindow(tk.Frame):

    def __init__(self,parent):

        super().__init__(parent)

        Router.load_registry()

        self.pack(
            fill="both",
            expand=True
        )

        self.create_layout()


    def create_layout(self):

        self.topbar=tk.Frame(
            self,
            height=50
        )
        self.topbar.pack(
            fill="x"
        )

        tk.Label(
            self.topbar,
            text="AGS-STUDIO | Enterprise Autonomous ERP",
            font=("Arial",16,"bold")
        ).pack(
            pady=10
        )


        self.sidebar=tk.Frame(
            self,
            width=200
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )


        self.workspace=tk.Frame(
            self
        )
        self.workspace.pack(
            side="right",
            fill="both",
            expand=True
        )


        self.create_menu()


    def create_menu(self):

        items=[
            ("Dashboard","dashboard"),
            ("Companies","companies"),
            ("Users","users"),
            ("Customers","customers"),
            ("Suppliers","suppliers"),
            ("Projects","projects"),
            ("Inventory","inventory"),
            ("Finance","finance"),
            ("Reports","reports"),
            ("AI Builder","ai_builder"),
            ("Autonomous Engine","autonomous")
        ]

        for label,route in items:

            tk.Button(
                self.sidebar,
                text=label,
                width=22,
                command=lambda r=route:self.open_page(r)
            ).pack(
                fill="x",
                pady=2
            )


    def open_page(self,route):

        for widget in self.workspace.winfo_children():
            widget.destroy()


        page=Router.load(
            route,
            self.workspace
        )

        if page:
            page.pack(
                fill="both",
                expand=True
            )
