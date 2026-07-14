from app.ai.autonomous.master_runtime import master_runtime
from app.ai.autonomous.agent_intelligence import agent_intelligence


class SelfLearningRuntime:

    def __init__(self):

        self.runtime = master_runtime
        self.intelligence = agent_intelligence



    def run(self, request):

        print("\n================================")
        print(" AGS SELF LEARNING RUNTIME V1")
        print("================================")


        context = self.intelligence.context()


        print("[MEMORY CONTEXT]")
        print(
            f"Previous executions: {len(context)}"
        )


        result = self.runtime.run(request)


        self.intelligence.learn(
            request,
            result
        )


        print("[LEARNING UPDATE COMPLETE]")


        return {
            "request": request,
            "memory_size": len(
                self.intelligence.context()
            ),
            "result": result
        }



self_learning_runtime = SelfLearningRuntime()
