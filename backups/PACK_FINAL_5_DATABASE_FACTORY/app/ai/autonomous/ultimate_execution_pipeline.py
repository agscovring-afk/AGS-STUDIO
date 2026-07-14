
from app.ai.autonomous.ultimate_agent_bridge import ultimate_bridge
from app.ai.autonomous.factory_connector import factory_connector


class UltimateExecutionPipeline:


    def execute(self,tasks):


        results=[]


        for task in tasks:


            print(
                "\n[ULTIMATE AGENT EXECUTION]"
            )


            result = ultimate_bridge.execute(
                task
            )


            factory_connector.consume(
                result
            )


            results.append(
                result
            )


        return results



ultimate_pipeline = UltimateExecutionPipeline()
