class UISelfBuildLoop:

    def __init__(self, generator=None, validator=None):
        self.generator = generator
        self.validator = validator


    def build(self, specification):

        ui = None

        if self.generator:
            ui = self.generator.generate(specification)

        if self.validator:
            result = self.validator.validate(ui)
        else:
            result = True

        if not result:
            return self.repair(ui)

        return ui


    def repair(self, ui):

        return ui
