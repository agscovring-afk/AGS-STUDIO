class EnterpriseEngine:

    def status(self):

        return {
            "system":
            "AGS ENTERPRISE ENGINE",

            "modules":[
                "MULTI_COMPANY",
                "MULTI_USER",
                "PERMISSIONS",
                "AUDIT_LOGS",
                "BACKUP",
                "CLOUD_SYNC",
                "API_GATEWAY"
            ],

            "status":
            "ACTIVE"
        }


engine = EnterpriseEngine()
