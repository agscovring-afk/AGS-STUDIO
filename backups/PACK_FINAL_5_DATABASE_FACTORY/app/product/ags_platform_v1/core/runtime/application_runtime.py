class ApplicationRuntime:

    def __init__(self):
        self.modules = {}
        self.running = False

    def register_module(self, name, module):
        self.modules[name] = module

    def start(self):
        self.running = True
        return "AGS RUNTIME STARTED"

    def stop(self):
        self.running = False
