"""
AGS Decision Memory
Persistent AI Decision Storage
"""

import json
import os
from datetime import datetime


DECISION_FILE = "app/ai/memory/decision_memory.json"


class DecisionMemory:


    def __init__(self):

        folder = os.path.dirname(
            DECISION_FILE
        )

        os.makedirs(
            folder,
            exist_ok=True
        )

        if not os.path.exists(
            DECISION_FILE
        ):

            self.save([])



    def load(self):

        with open(
            DECISION_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)



    def save(self, data):

        with open(
            DECISION_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )



    def add(self, decision):

        decisions = self.load()


        decisions.append(
            {
                "timestamp": str(
                    datetime.now()
                ),
                "decision": decision
            }
        )


        self.save(
            decisions
        )


        return decision



    def get(self):

        return self.load()



memory = DecisionMemory()