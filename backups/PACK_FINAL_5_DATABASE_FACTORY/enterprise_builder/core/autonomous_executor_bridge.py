from enterprise_builder.core.action_executor import EnterpriseActionExecutor


class AutonomousEnterpriseExecutor:


    def __init__(self):

        self.executor = EnterpriseActionExecutor()


    def run(self, task):

        return self.executor.execute(task)