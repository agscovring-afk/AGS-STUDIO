class CommandPalette:

    def __init__(self):

        self.commands = {}

    def register(self, name, callback):

        self.commands[name] = callback

    def execute(self, name, *args, **kwargs):

        if name in self.commands:
            return self.commands[name](*args, **kwargs)
