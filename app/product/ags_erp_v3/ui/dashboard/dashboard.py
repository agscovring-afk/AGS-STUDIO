class Dashboard:

    def __init__(self):
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    def render(self):
        return {
            "title": "AGS ERP V3 DASHBOARD",
            "widgets": self.widgets
        }
