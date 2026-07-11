from app.product.ags_erp_v3.ui.modules.erp_module_screens import ERPModuleScreens


class AGSERPV3DesktopApp:

    def __init__(self):
        self.modules = ERPModuleScreens()


    def boot(self):
        return "AGS ERP V3 DESKTOP APP READY"


    def modules_list(self):
        return self.modules.list()
