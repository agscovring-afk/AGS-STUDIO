class AutonomousRuntime:

    def __init__(self, engine=None):

        self.engine = engine
        self.context = None


    def connect_engine(self, engine):

        self.engine = engine


    def execute(self, task):

        if self.engine:

            return self.engine.run(task)


        return {
            "status": "no_engine",
            "task": task
        }
