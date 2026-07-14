class UIFramework:

    def __init__(self):

        self.components = {}
        self.layouts = {}
        self.panels = {}

    def register_component(self, name, component):
        self.components[name] = component

    def register_layout(self, name, layout):
        self.layouts[name] = layout

    def register_panel(self, name, panel):
        self.panels[name] = panel
