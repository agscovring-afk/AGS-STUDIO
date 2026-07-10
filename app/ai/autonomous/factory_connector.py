
from pathlib import Path
import json


class AGSFactoryConnector:


    def consume(self,agent_output):


        folder = Path(
            "factory_outputs"
        )

        folder.mkdir(
            exist_ok=True
        )


        agent = agent_output.get(
            "agent",
            "unknown"
        )


        file = folder / (
            agent + "_factory.json"
        )


        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(
                agent_output,
                f,
                indent=4,
                ensure_ascii=False
            )


        return {

            "factory_status":
            "stored",

            "file":
            str(file)

        }



factory_connector = AGSFactoryConnector()
