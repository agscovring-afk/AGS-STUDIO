class ConstructionModulePlanner:


    def plan(self, task):

        text = task.lower()

        if any(
            x in text
            for x in [
                "construction",
                "facade",
                "aluminium",
                "curtain wall",
                "glass"
            ]
        ):

            return [
                "projects",
                "tenders",
                "boq",
                "contracts",
                "suppliers",
                "procurement",
                "cost_control",
                "workers",
                "equipment"
            ]


        if "erp" in text:

            return [
                "customers",
                "products",
                "orders",
                "invoices",
                "accounting"
            ]


        return []
