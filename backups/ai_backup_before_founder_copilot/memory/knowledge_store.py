"""
AGS Knowledge Store
Autonomous Learning Database
"""

import json
from pathlib import Path
from datetime import datetime


class KnowledgeStore:


    def __init__(self):

        self.path = Path("data/knowledge_store.json")

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.path.exists():
            self.save([])



    def load(self):

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def save(self,data):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )



    def store(self,item):

        data=self.load()

        data.append(
            {
                "timestamp":
                str(datetime.now()),

                "data":
                item
            }
        )

        self.save(data)



    def store_execution(self,task,result):

        self.store(
            {
                "type":
                "execution_result",

                "task":
                task,

                "result":
                result
            }
        )



    def search(self,keyword=None):

        data=self.load()

        if not keyword:
            return data

        results=[]

        for item in data:

            text=str(item).lower()

            if keyword.lower() in text:
                results.append(item)

        return results



store=KnowledgeStore()
