from app.product.ags_erp_v3.ui.modules.module_screen import ModuleScreen


class ERPModuleScreens:

    MODULES = [
        "Dashboard",
        "CRM",
        "Projects",
        "Suppliers",
        "Inventory",
        "Purchasing",
        "Quotations",
        "Invoices",
        "Accounting",
        "HR",
        "Reports"
    ]


    def __init__(self):
        self.screens = {
            module: ModuleScreen(module)
            for module in self.MODULES
        }


    def list(self):
        return list(self.screens.keys())


    def open(self, module):
        return self.screens[module].render()
