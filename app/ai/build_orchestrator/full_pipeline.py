
import json

from app.ai.ast_engine.bridge import bridge as ast
from app.ai.project_memory.v2.bridge import bridge as memory
from app.ai.code_understanding.v2.bridge import bridge as understanding


class FullBuildPipeline:


    def execute(self,request):

        print('==============================')
        print('AGS FULL BUILD PIPELINE CONNECTOR V1')
        print('==============================')


        report={}

        report['AST']=ast.execute(request)

        report['MEMORY']=memory.execute(request)

        report['UNDERSTANDING']=understanding.execute(request)


        with open(
            'data/build_execution_report.json',
            'w',
            encoding='utf-8'
        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )


        report['status']='COMPLETED'

        return report



pipeline=FullBuildPipeline()
