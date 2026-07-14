from app.ai.orchestrator.request_analyzer import analyzer
from app.ai.orchestrator.task_router import router
from app.ai.orchestrator.agent_dispatcher import dispatcher
from app.ai.orchestrator.result_collector import collector


class MasterOrchestrator:


    def run(self, request):

        analysis = analyzer.analyze(request)

        route = router.route(analysis)

        result = dispatcher.dispatch(
            "ARCHITECT_AGENT",
            route["task"]
        )

        return collector.collect(result)


orchestrator = MasterOrchestrator()
