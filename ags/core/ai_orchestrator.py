from datetime import datetime


class AIOrchestrator:


    def __init__(self, agent_manager):

        self.agent_manager = agent_manager


    def run_team(self, module):

        agents = [

            "architect",
            "backend",
            "database",
            "ui",
            "testing",
            "documentation"

        ]


        report = {

            "module": module,

            "time":
                str(datetime.now()),

            "agents": {}

        }


        print("=== AI ORCHESTRATOR ===")


        for agent in agents:

            try:

                print()
                print(
                    "Running:",
                    agent
                )


                result = self.agent_manager.run(
                    agent,
                    module
                )


                report["agents"][agent] = {

                    "status": "OK",

                    "result": result

                }


                print(
                    agent,
                    "OK"
                )


            except Exception as error:


                report["agents"][agent] = {

                    "status": "FAILED",

                    "error": str(error)

                }


                print(

                    agent,

                    "FAILED - CONTINUING"

                )


        print()

        print(
            "AI TEAM FINISHED"
        )


        return report
