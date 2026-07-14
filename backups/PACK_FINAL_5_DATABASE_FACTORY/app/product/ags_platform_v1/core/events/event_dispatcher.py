class EventDispatcher:

    def __init__(self):
        self.events = {}

    def subscribe(self, event, callback):
        self.events.setdefault(event, []).append(callback)

    def emit(self, event, data=None):
        for callback in self.events.get(event, []):
            callback(data)
