
class ERPActivationV1:

    modules = [
        "Companies",
        "Users",
        "Clients",
        "Suppliers",
        "Projects",
        "Catalogue",
        "Purchases",
        "Warehouse",
        "Invoices",
        "Payments",
        "Reports"
    ]

    def activate(self):
        return self.modules
