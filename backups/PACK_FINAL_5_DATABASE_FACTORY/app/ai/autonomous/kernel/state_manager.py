class StateManager:

    def __init__(self):

        self.state = {}


    def set(self, key, value):

        self.state[key] = value


    def get(self, key, default=None):

        return self.state.get(
            key,
            default
        )


    def all(self):

        return self.state


state_manager = StateManager()