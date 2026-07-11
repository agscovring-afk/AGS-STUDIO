class ResponsiveLayoutEngine:

    def __init__(self):

        self.layouts = {}

    def register(self, name, layout):

        self.layouts[name] = layout

    def resolve(self, width):

        if width < 700:
            return "mobile"

        if width < 1200:
            return "tablet"

        return "desktop"
