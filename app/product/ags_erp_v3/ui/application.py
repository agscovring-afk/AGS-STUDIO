from app.product.ags_erp_v3.ui.menu.main_menu import MainMenu
from app.product.ags_erp_v3.ui.dashboard.dashboard import Dashboard
from app.product.ags_erp_v3.ui.modules.erp_module_screens import ERPModuleScreens


class AGSERPV3DesktopApp:

    def __init__(self):
        self.menu = MainMenu()
        self.dashboard = Dashboard()
        self.modules = ERPModuleScreens()


    def boot(self):
        return "AGS ERP V3 APPLICATION READY"


    def list_modules(self):
        return self.modules.list()


    def modules_list(self):
        return self.modules.list()


    def open_module(self, module):
        return self.modules.open(module)



class AGSERPV3Application(AGSERPV3DesktopApp):
    pass