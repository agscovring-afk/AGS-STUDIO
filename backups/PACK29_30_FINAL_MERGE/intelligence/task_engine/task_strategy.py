class TaskStrategy:

    def build(self, domain):

        profile = domain["profile"]

        if profile == "construction_facade":

            return [
                ("analyze_construction_domain",
                 "Analyze construction business domain",
                 10),

                ("design_facade_erp_architecture",
                 "Design facade ERP architecture",
                 9),

                ("generate_construction_modules",
                 "Generate construction modules",
                 8),

                ("build_tender_management",
                 "Create tender management system",
                 7),

                ("validate_construction_platform",
                 "Validate enterprise construction platform",
                 6)
            ]

        if profile == "enterprise":

            return [
                ("analyze_business_domain",
                 "Analyze enterprise domain",
                 10),

                ("design_system_architecture",
                 "Design enterprise architecture",
                 9),

                ("generate_modules",
                 "Generate ERP modules",
                 8),

                ("validate_system",
                 "Validate generated system",
                 7)
            ]

        return [
            ("analyze_request",
             domain["request"],
             5)
        ]
