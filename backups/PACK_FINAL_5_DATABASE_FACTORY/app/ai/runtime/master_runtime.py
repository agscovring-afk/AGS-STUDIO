from app.ai.runtime.request_pipeline import pipeline
from app.ai.runtime.agent_flow import flow
from app.ai.runtime.factory_trigger import trigger
from app.ai.runtime.report_generator import reporter


class MasterRuntime:


    def run(self, request):


        pipeline_result = pipeline.process(request)


        agent_result = flow.execute(request)


        factory_result = trigger.build(request)


        final = {

            "request":
            request,

            "pipeline":
            pipeline_result,

            "agents":
            agent_result,

            "factory":
            factory_result
        }


        report = reporter.create(final)


        final["report"] = report


        return final



runtime = MasterRuntime()
