from app.ai.master_core.engine import engine
from app.ai.planner.task_generator import generator


class RequestPipeline:


    def process(self, request):

        analysis = engine.analyze(request)

        tasks = generator.generate(request)

        return {
            "analysis": analysis,
            "tasks": tasks
        }


pipeline = RequestPipeline()
