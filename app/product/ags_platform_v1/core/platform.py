from app.product.ags_platform_v1.core.runtime.application_runtime import ApplicationRuntime
from app.product.ags_platform_v1.core.registry.module_registry import ModuleRegistry


class AGSPlatform:

    def __init__(self):
        self.runtime = ApplicationRuntime()
        self.registry = ModuleRegistry()

    def boot(self):
        self.runtime.start()
        return "AGS PLATFORM V1 BOOTED"
