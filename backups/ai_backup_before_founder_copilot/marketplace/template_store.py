class TemplateStore:

    def list(self):

        return {
            "templates":
            [
                "CONSTRUCTION",
                "ALUMINIUM",
                "FACADE",
                "MANUFACTURING"
            ],
            "status":"READY"
        }


store = TemplateStore()
