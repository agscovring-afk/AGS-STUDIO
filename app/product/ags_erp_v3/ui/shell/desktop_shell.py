class ERPDesktopShell:

    def __init__(self):
        self.title = "AGS ERP V3 ENTERPRISE"
        self.modules = []

    def register_module(self, module):
        self.modules.append(module)

    def start(self):
        return "AGS ERP V3 DESKTOP SHELL RUNNING"
