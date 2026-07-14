import json
from pathlib import Path

class Reporter:

    def create(self, data):

        Path("reports").mkdir(exist_ok=True)

        Path("reports/build_report.json").write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

        return data


reporter = Reporter()