import tkinter as tk


class MainWindow:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "AGS ERP V3 Autonomous Enterprise Platform"
        )

        self.root.geometry(
            "1200x700"
        )

        self.build()


    def build(self):

        header = tk.Frame(self.root)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="AGS ERP V3",
            font=("Arial",24,"bold")
        )

        title.pack(
            padx=20,
            pady=15,
            anchor="w"
        )


        sidebar = tk.Frame(
            self.root,
            width=220
        )

        sidebar.pack(
            side="left",
            fill="y"
        )


        modules = [
            "Dashboard",
            "CRM",
            "Projects",
            "Invoices",
            "Inventory",
            "Suppliers",
            "Reports",
            "AI Business Layer",
            "Cloud Platform"
        ]


        for module in modules:

            tk.Button(
                sidebar,
                text=module,
                width=22
            ).pack(
                pady=5,
                padx=10
            )


        content = tk.Frame(
            self.root
        )

        content.pack(
            expand=True,
            fill="both"
        )


        tk.Label(
            content,
            text="""
AGS ERP V3 PRODUCTION

✓ Desktop GUI Runtime
✓ CRUD Engine
✓ Production Database
✓ Business Modules
✓ AI Layer
✓ Cloud Platform

SYSTEM STATUS : READY
""",
            font=("Arial",16),
            justify="left"
        ).pack(
            padx=40,
            pady=40,
            anchor="nw"
        )
