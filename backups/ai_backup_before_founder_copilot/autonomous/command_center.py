
from app.ai.autonomous.self_learning_runtime import self_learning_runtime


class AGSCommandCenter:

    def __init__(self):
        self.runtime = self_learning_runtime


    def execute(self, request):

        print("\n================================")
        print(" AGS AUTONOMOUS V2 COMMAND CENTER")
        print("================================")

        result = self.runtime.run(request)

        print("\n[COMMAND COMPLETE]")

        return result


ags_command = AGSCommandCenter()
