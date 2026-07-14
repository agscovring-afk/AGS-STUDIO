
import json
from pathlib import Path


class ReleaseReport:


    def create(self, result):

        path = Path(
            "workspace/release_report.json"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        path.write_text(
            json.dumps(
                result,
                indent=4
            ),
            encoding="utf-8"
        )


        return path
