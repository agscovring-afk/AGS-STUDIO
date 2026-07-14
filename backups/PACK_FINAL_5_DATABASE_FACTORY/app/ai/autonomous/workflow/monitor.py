from datetime import datetime


class WorkflowMonitor:


    def __init__(self):

        self.logs = []


    def record(self, event):

        self.logs.append(
            {
                "event": event,
                "time": datetime.now().isoformat()
            }
        )


    def history(self):

        return self.logs



monitor = WorkflowMonitor()