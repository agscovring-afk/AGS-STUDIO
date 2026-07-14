class RecoverySystem:


    def recover(self, error):

        return {
            "status":
            "RECOVERY_STARTED",
            "error":
            str(error)
        }


recovery = RecoverySystem()
