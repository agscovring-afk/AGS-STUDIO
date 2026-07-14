
from app.ai.build_orchestrator.full_pipeline import pipeline
from app.ai.test_quality.v1.bridge import bridge as quality
from app.ai.deployment.v1.bridge import bridge as deploy


class MasterControlV1:


    def execute(self,request):


        result={}


        if 'BUILD' in str(request).upper():

            result['BUILD'] = pipeline.execute(request)


        result['QUALITY'] = quality.execute(request)

        result['DEPLOYMENT'] = deploy.execute(request)


        result['status']='COMPLETED'


        return result



bridge=MasterControlV1()
