import os
from .analyzer import ASTAnalyzer


class ASTExecutionBridge:


    def execute(self,request):

        print("==============================")
        print("AGS AST ANALYZER BRIDGE V1")
        print("==============================")


        analyzer=ASTAnalyzer(os.getcwd())

        result=analyzer.scan()

        output=analyzer.save()


        return {
            "engine":"AGS AST ANALYZER V1",
            "request":request,
            "status":"COMPLETED",
            "files":len(result["files"]),
            "classes":len(result["classes"]),
            "functions":len(result["functions"]),
            "output":output
        }



bridge=ASTExecutionBridge()
