class ThemeEngine:

    def __init__(self):

        self.current_theme = "dark"

    def set_theme(self, name):

        self.current_theme = name

    def get_theme(self):

        return self.current_theme
