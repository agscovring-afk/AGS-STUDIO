from datetime import datetime


class SecurityAudit:

    def __init__(self):
        self.events = []

    def record(self, event, user=None):
        self.events.append({
            "event": event,
            "user": user,
            "timestamp": datetime.utcnow().isoformat()
        })
