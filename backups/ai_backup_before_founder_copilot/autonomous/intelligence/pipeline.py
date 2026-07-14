class IntelligencePipeline:


    def execute(self, request):

        from .system import system

        return system.run(request)


pipeline = IntelligencePipeline()
