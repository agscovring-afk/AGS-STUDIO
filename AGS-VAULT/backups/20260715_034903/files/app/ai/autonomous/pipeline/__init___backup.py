from .erp_pipeline import ERPFullPipeline


class AutonomousPipeline:

    def __init__(
        self,
        engine=None,
        planner=None,
        router=None,
        executor=None,
        validator=None
    ):
        self.engine = engine
        self.planner = planner
        self.router = router
        self.executor = executor
        self.validator = validator

        self.pipeline = ERPFullPipeline()


    def run(self, task):

        return self.execute(task)


    def execute(self, request):

        text = str(request).upper()

        if "AST ANALYZER" in text:
            return execute_ast(request)

        if "CEO PLATFORM" in text or "CEO" in text:
            return execute_ceo(request)

        return {
            "pipeline": self.pipeline.name,
            "request": request,
            "status": "READY"
        }
from .ast_router import execute_ast
from .ceo_router import execute_ceo
