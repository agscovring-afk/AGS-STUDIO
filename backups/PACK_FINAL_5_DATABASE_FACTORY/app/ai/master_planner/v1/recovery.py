class RecoveryManager:

    def recover(self, task, error):

        print()

        print("[RECOVERY]")

        print(task.name)

        print(error)

        task.status = "failed"

        task.error = str(error)

        return task
