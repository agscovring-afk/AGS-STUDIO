class ExecutionGuard:
    def validate(self):
        return True

class ChangeValidator:
    def check(self):
        return True

class RollbackManager:
    def rollback(self):
        return True

class AutonomousPolicy:
    def allow(self):
        return True
