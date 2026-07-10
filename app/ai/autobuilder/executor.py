from datetime import datetime

class Executor:

    def run(self, plan):

        result = []

        for phase in plan["phases"]:
            result.append({
                "phase": phase,
                "status": "completed",
                "time": str(datetime.now())
            })

        return result


executor = Executor()