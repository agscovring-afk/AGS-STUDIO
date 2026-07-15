from pathlib import Path
import json


class EnterpriseValidator:


    def validate(self):

        result = {

            "generator": Path("enterprise_output").exists(),

            "registry": Path("enterprise_registry.json").exists(),

            "config": Path("enterprise_config.json").exists(),

            "manifest": Path("enterprise_registry.json").exists()

        }


        result["status"] = (
            "READY"
            if all(result.values())
            else "FAILED"
        )


        return result