class TaskValidator:

    def validate(self, task):

        if task is None:

            return {
                "success": False,
                "message": "Task is empty"
            }


        return {
            "success": True,
            "message": "Task valid"
        }



class AutonomousValidator:


    def validate(self, result):

        if result is None:

            return {
                "success": False,
                "message": "Empty result"
            }


        if isinstance(result, dict):

            if result.get("status") in [
                "completed",
                "success"
            ]:

                return {
                    "success": True,
                    "message": "Validation passed"
                }


            if result.get("status") == "no_agent":

                return {
                    "success": False,
                    "message": "Agent not found"
                }


        return {
            "success": True,
            "message": "Basic validation passed"
        }



validator = AutonomousValidator()
task_validator = TaskValidator()
