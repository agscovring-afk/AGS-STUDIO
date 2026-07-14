class AutonomousUIBridge:

    def __init__(self, engine=None):

        self.engine = engine

    def connect(self, engine):

        self.engine = engine

    def send(self, task):

        if self.engine:

            return self.engine.run(task)

        return None
