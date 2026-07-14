import json
from datetime import datetime


class AutonomousBuildReport:

    def generate(self, execution_result):

        report = {
            "system": "AGS AUTONOMOUS V2",
            "timestamp": str(datetime.now()),
            "status": execution_result.get("status"),
            "execution": execution_result
        }

        with open(
            "autonomous_build_report.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                report,
                f,
                indent=4,
                ensure_ascii=False,
                default=str
            )


        print("[FINAL REPORT GENERATED]")

        return report


build_report = AutonomousBuildReport()
