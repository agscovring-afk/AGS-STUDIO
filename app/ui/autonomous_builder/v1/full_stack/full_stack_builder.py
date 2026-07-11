class FullStackAutonomousBuilder:


    def __init__(self, ui_builder=None, app_generator=None):

        self.ui_builder = ui_builder
        self.app_generator = app_generator


    def build(self, blueprint):

        application = None

        if self.app_generator:
            application = self.app_generator.generate(
                blueprint
            )

        return {
            "status":"completed",
            "application":application
        }
