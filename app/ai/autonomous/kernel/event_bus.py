from datetime import datetime


class EventBus:

    def __init__(self):

        self.events = []


    def emit(self, name, data=None):

        event = {
            "event": name,
            "data": data,
            "time": datetime.now().isoformat()
        }

        self.events.append(event)

        return event


    def history(self):

        return self.events


event_bus = EventBus()