import json
import os
from datetime import datetime


MEMORY_FILE = "app/ai/memory/project_memory.json"


class MemoryManager:


    def __init__(self):

        folder = os.path.dirname(
            MEMORY_FILE
        )

        os.makedirs(
            folder,
            exist_ok=True
        )


        if not os.path.exists(MEMORY_FILE):

            self.save([])



    def load(self):

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def save(self, data):

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )



    def remember(self, module, action, details):

        memory = self.load()


        memory.append({

            "date":
                str(datetime.now()),

            "module":
                module,

            "action":
                action,

            "details":
                details

        })


        self.save(memory)



    def get_module_memory(self, module):

        memory = self.load()


        return [

            item for item in memory

            if item["module"] == module

        ]