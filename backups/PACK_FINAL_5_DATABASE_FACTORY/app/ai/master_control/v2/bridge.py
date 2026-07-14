
from app.ai.software_factory.v2.bridge import bridge as factory


class MasterControlV2:


    def execute(self,request):

        return factory.execute(request)



bridge=MasterControlV2()
