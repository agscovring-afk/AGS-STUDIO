import json
import os


class ReportGenerator:


    def create(self, data):

        os.makedirs(
            "reports",
            exist_ok=True
        )

        file="reports/autonomous_runtime_report.json"


        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )


        return {
            "report":file,
            "status":"CREATED"
        }


reporter = ReportGenerator()
