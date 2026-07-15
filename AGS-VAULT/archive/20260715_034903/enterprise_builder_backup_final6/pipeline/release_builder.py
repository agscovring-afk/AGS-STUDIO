from pathlib import Path
from datetime import datetime


class ReleaseBuilder:

    def build(self):

        release = Path(
            "enterprise_output/releases/release.json"
        )

        release.write_text(
            '{"release":"READY","date":"'
            + datetime.now().isoformat()
            + '"}'
        )

        return {
            "release": "READY"
        }