from .shell.desktop_shell import ERPDesktopShell
from .menu.main_menu import MainMenu
from .dashboard.dashboard import Dashboard
from .modules.module_screen import ModuleScreen


class AGSERPV3Application:

    def __init__(self):
        self.shell = ERPDesktopShell()
        self.menu = MainMenu()
        self.dashboard = Dashboard()

    def boot(self):

        modules = [
            "CRM",
            "PROJECTS",
            "SUPPLIERS",
            "INVENTORY",
            "PURCHASING",
            "QUOTATIONS",
            "INVOICES",
            "ACCOUNTING",
            "HR",
            "REPORTS"
        ]

        for module in modules:
            self.menu.add(module)
            self.shell.register_module(module)

        return "AGS ERP V3 APPLICATION READY"
