class UIHotReload:

    def __init__(self):

        self.version = 0


    def reload(self, ui):

        self.version += 1

        return {
            "version": self.version,
            "ui": ui
        }
