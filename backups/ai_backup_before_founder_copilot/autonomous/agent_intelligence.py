import json
import os
from datetime import datetime


MEMORY_FILE = "data/autonomous_intelligence_memory.json"


class IntelligenceMemory:

    def __init__(self):

        folder = os.path.dirname(MEMORY_FILE)

        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.exists(MEMORY_FILE):

            with open(
                MEMORY_FILE,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump([], f)



    def save(self, request, result):

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            memory = json.load(f)


        memory.append({

            "timestamp": str(datetime.now()),
            "request": request,
            "result": result

        })


        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                memory,
                f,
                indent=4,
                ensure_ascii=False,
                default=str
            )



    def recall(self):

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



intelligence_memory = IntelligenceMemory()



class AgentIntelligenceLayer:


    def __init__(self):

        self.memory = intelligence_memory



    def learn(self, request, result):

        print("[INTELLIGENCE MEMORY UPDATE]")

        self.memory.save(
            request,
            result
        )



    def context(self):

        return self.memory.recall()



agent_intelligence = AgentIntelligenceLayer()
