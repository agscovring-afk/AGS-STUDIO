class RuntimeManager:

    def __init__(self):
        self.state = "READY"

    def start(self):
        self.state = "RUNNING"

    def stop(self):
        self.state = "STOPPED"

    def status(self):
        return self.state
