class UIGenerationPipeline:

    def __init__(self):

        self.steps = []


    def register(self, step):

        self.steps.append(step)


    def execute(self, specification):

        result = specification

        for step in self.steps:

            result = step.process(result)

        return result
