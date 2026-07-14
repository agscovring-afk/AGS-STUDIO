from datetime import datetime


class CollaborationReport:

    def __init__(self):
        self.events = []

    def add(self, event):
        self.events.append(
            {
                "event": event,
                "time": datetime.now().isoformat()
            }
        )

    def generate(self):
        return {
            "system": "AGS AUTONOMOUS V2",
            "type": "COLLABORATION REPORT",
            "events": self.events,
            "count": len(self.events)
        }


report = CollaborationReport()