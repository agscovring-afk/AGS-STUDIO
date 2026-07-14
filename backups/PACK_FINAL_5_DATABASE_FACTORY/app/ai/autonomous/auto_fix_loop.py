class AutoFixLoop:

    def __init__(self):
        self.max_attempts = 3


    def execute_with_fix(self, executor, task):

        attempts = 0

        while attempts < self.max_attempts:

            print(f"\n[AUTO FIX LOOP] Attempt {attempts + 1}")

            result = executor.execute_task(task)

            if result.get("status") == "completed":
                return result

            attempts += 1

            print("[AUTO FIX] Retrying task...")


        return {
            "status": "failed",
            "task": task.name,
            "message": "Maximum fix attempts reached"
        }


auto_fix_loop = AutoFixLoop()
