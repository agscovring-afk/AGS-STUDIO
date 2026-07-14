from .builder import KnowledgeGraphBuilder


class KnowledgeGraphBridge:


    def execute(self,request):

        print("==============================")
        print("AGS KNOWLEDGE GRAPH BUILDER V1")
        print("==============================")


        builder=KnowledgeGraphBuilder()

        graph=builder.build()

        output=builder.save()


        return {

            "engine":"AGS KNOWLEDGE GRAPH V1",

            "request":str(request),

            "status":"COMPLETED",

            "nodes":len(graph["nodes"]),

            "relations":len(graph["relations"]),

            "output":output

        }



bridge=KnowledgeGraphBridge()
