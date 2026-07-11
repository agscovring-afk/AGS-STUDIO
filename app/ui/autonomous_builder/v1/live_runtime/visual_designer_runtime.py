class VisualDesignerRuntime:

    def __init__(self):

        self.widgets = []
        self.layouts = []


    def load(self, ui_definition):

        self.definition = ui_definition

        return self.definition


    def add_widget(self, widget):

        self.widgets.append(widget)


    def add_layout(self, layout):

        self.layouts.append(layout)
