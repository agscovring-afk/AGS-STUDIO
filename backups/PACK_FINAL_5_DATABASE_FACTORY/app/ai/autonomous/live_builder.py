from app.ai.autonomous.master_runtime import master_runtime


class LiveAutonomousBuilder:

    def __init__(self):
        self.runtime = master_runtime


    def build(self, request):

        print("\n================================")
        print(" AGS AUTONOMOUS LIVE BUILDER V1")
        print("================================")


        print("[BUILD REQUEST]")
        print(request)


        result = self.runtime.run(request)


        print("\n[BUILD FINISHED]")


        return result



live_builder = LiveAutonomousBuilder()
