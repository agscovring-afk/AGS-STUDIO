
from app.product.ags_erp_v3.desktop_app.router import Router
from app.product.ags_erp_v3.desktop_app.components.workspace import Workspace


class GUINavigationIntegrationV1:

    def __init__(self):

        self.workspace = Workspace()
        self.router = Router(self.workspace)

        self.register_pages()


    def register_pages(self):

        modules = [
            "Dashboard",
            "CRM",
            "Projects",
            "Invoices",
            "Inventory",
            "Reports"
        ]

        for module in modules:
            self.router.register(
                module,
                lambda m=module: f"{m} MODULE SCREEN READY"
            )


    def click(self, button):

        print("[SIDEBAR CLICK]", button)

        if self.router.navigate(button):
            print("[PAGE LOADED]", button)
            print("[DISPLAY] MODULE SCREEN")
            return True

        print("[ERROR] ROUTE NOT FOUND")
        return False


if __name__ == "__main__":

    app = GUINavigationIntegrationV1()

    for item in [
        "Dashboard",
        "CRM",
        "Projects",
        "Invoices",
        "Inventory",
        "Reports"
    ]:
        app.click(item)
