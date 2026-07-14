class ModuleMarketplace:

    def list(self):

        return {
            "modules":
            [
                "ERP MODULES",
                "BUSINESS MODULES",
                "CUSTOM MODULES"
            ],
            "status":"READY"
        }


marketplace = ModuleMarketplace()
