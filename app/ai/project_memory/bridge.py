
import json,os

class ProjectMemoryBridge:

    def execute(self,request):

        os.makedirs('data',exist_ok=True)

        memory={
            'project':'AGS-STUDIO',
            'context':'AST + Knowledge Graph + Relations'
        }

        json.dump(memory,open('data/project_memory.json','w'),indent=4)

        return {
            'engine':'AGS PROJECT MEMORY V1',
            'status':'COMPLETED',
            'output':'data/project_memory.json'
        }

bridge=ProjectMemoryBridge()
