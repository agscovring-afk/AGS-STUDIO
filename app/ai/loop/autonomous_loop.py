from app.ai.loop.analyze import analyzer
from app.ai.loop.planner import planner
from app.ai.loop.builder import builder
from app.ai.loop.tester import tester
from app.ai.loop.report import reporter


class AutonomousLoop:


    def execute(self, request):

        a = analyzer.run(request)
        p = planner.run(a)
        b = builder.run(p)
        t = tester.run(b)

        return reporter.run({
            "analyze":a,
            "plan":p,
            "build":b,
            "test":t
        })


loop = AutonomousLoop()
