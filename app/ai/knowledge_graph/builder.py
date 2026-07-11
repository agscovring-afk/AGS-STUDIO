import json
import os


class KnowledgeGraphBuilder:


    def __init__(self, ast_file="data/project_ast.json"):

        self.ast_file=ast_file

        self.graph={
            "nodes":[],
            "relations":[]
        }



    def load(self):

        with open(
            self.ast_file,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def build(self):

        data=self.load()


        for file in data.get("files",[]):

            node={
                "type":"file",
                "name":str(file)
            }

            self.graph["nodes"].append(node)



        for cls in data.get("classes",[]):

            self.graph["nodes"].append({

                "type":"class",
                "name":cls

            })


        for fn in data.get("functions",[]):

            self.graph["nodes"].append({

                "type":"function",
                "name":fn

            })


        return self.graph



    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )


        output="data/project_knowledge_graph.json"


        with open(
            output,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.graph,
                f,
                indent=4
            )


        return output
