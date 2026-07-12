
import customtkinter as ctk

from app.product.ags_erp_v3.desktop_app.router import Router


class RealUINavigationBindingV1:

    def __init__(self, sidebar, workspace):

        self.sidebar = sidebar
        self.workspace = workspace

        self.router = Router(self.workspace)

        self.register_routes()
        self.bind_sidebar()


    def register_routes(self):

        pages = {

            "Dashboard": self.dashboard_page,
            "CRM": self.crm_page,
            "Projects": self.projects_page,
            "Inventory": self.inventory_page,
            "Invoices": self.invoices_page,
            "Reports": self.reports_page,

        }

        for name, page in pages.items():
            self.router.register(name, page)


    def bind_sidebar(self):

        if hasattr(self.sidebar, "buttons"):

            for name, button in self.sidebar.buttons.items():

                button.configure(
                    command=lambda n=name:
                    self.router.navigate(n)
                )


    def update_workspace(self, title):

        for widget in self.workspace.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(
            self.workspace,
            text=title,
            font=("Arial", 28)
        )

        label.pack(
            expand=True
        )


    def dashboard_page(self):
        self.update_workspace(
            "DASHBOARD SCREEN"
        )


    def crm_page(self):
        self.update_workspace(
            "CRM MODULE SCREEN"
        )


    def projects_page(self):
        self.update_workspace(
            "PROJECTS MODULE SCREEN"
        )


    def inventory_page(self):
        self.update_workspace(
            "INVENTORY MODULE SCREEN"
        )


    def invoices_page(self):
        self.update_workspace(
            "INVOICES MODULE SCREEN"
        )


    def reports_page(self):
        self.update_workspace(
            "REPORTS MODULE SCREEN"
        )
