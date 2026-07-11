from .engine import KnowledgeRelationEngine


class KnowledgeRelationBridge:


    def execute(self,request):

        print("==============================")
        print("AGS KNOWLEDGE RELATION ENGINE V1")
        print("==============================")


        engine=KnowledgeRelationEngine()


        graph=engine.build()


        output=engine.save()


        return {

            "engine":"AGS KNOWLEDGE RELATION ENGINE V1",

            "request":str(request),

            "status":"COMPLETED",

            "nodes":len(graph["nodes"]),

            "relations":len(graph["relations"]),

            "output":output

        }



bridge=KnowledgeRelationBridge()
