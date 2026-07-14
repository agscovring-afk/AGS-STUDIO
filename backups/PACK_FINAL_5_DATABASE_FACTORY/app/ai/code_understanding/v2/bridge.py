
import json,os


class CodeUnderstandingV2:


    def execute(self,request):

        with open(
            'data/project_ast.json',
            encoding='utf-8'
        ) as f:

            ast=json.load(f)


        analysis={

            'architecture':'detected',

            'modules':
            len(ast.get('files',[])),

            'classes':
            len(ast.get('classes',[])),

            'functions':
            len(ast.get('functions',[]))

        }


        with open(
            'data/architecture_analysis.json',
            'w',
            encoding='utf-8'
        ) as f:

            json.dump(
                analysis,
                f,
                indent=4
            )


        return {

            'engine':'AGS CODE UNDERSTANDING V2',

            'status':'COMPLETED',

            'analysis':analysis,

            'output':
            'data/architecture_analysis.json'

        }


bridge=CodeUnderstandingV2()
