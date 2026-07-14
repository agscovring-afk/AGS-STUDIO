
import json
from pathlib import Path
from datetime import datetime


class RepairHistory:


    def __init__(self):
        self.file = Path("workspace/repair_history.json")
        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


    def save(self, data):

        history = []

        if self.file.exists():

            history = json.loads(
                self.file.read_text(
                    encoding="utf-8"
                )
            )


        data["timestamp"] = str(
            datetime.now()
        )

        history.append(data)


        self.file.write_text(
            json.dumps(
                history,
                indent=4
            ),
            encoding="utf-8"
        )
