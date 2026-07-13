from .workers.bridge import bridge


class RealAgentEngine:


    def run(self, plan):

        results = []


        for item in plan:

            worker = item.get("worker")
            task = item.get("task")


            result = bridge.dispatch(
                worker,
                task
            )


            results.append(result)


        return {

            "engine":
            "REAL AGENT ENGINE V1",

            "executions":
            results
        }



engine = RealAgentEngine()


real_agent_engine = RealAgentEngine()
