
from app.ai.ast_engine.bridge import bridge as ast_bridge


class BuildOrchestratorBridge:


    def execute(self,request):

        print("==============================")
        print("AGS AUTONOMOUS BUILD PIPELINE V1")
        print("==============================")


        result={}

        text=str(request)


        if "BUILD PROJECT" in text.upper():

            result["AST"]=ast_bridge.execute(
                "BUILD PROJECT AST ANALYSIS"
            )


        result["pipeline"]="AUTONOMOUS BUILD EXECUTION"

        result["status"]="COMPLETED"


        return result



bridge=BuildOrchestratorBridge()
