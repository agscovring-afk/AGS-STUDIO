from pathlib import Path
import json
from datetime import datetime


class EnterpriseReport:


    def generate(self, data):

        report = {

            "timestamp": datetime.now().isoformat(),

            "enterprise_status": data

        }


        Path(
            "enterprise_output/enterprise_report.json"
        ).write_text(
            json.dumps(
                report,
                indent=4
            )
        )


        return report