from pathlib import Path


class ProductionGuard:


    def check(self):

        required=[

            "enterprise_builder",

            "enterprise_registry.json",

            "enterprise_config.json",

            "enterprise_output"

        ]


        result={}

        for item in required:

            result[item]=Path(item).exists()


        result["ready"]=all(
            result.values()
        )


        return result