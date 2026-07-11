import json
import os


class KnowledgeRelationEngine:


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


        files=data.get("files",[])

        classes=data.get("classes",[])

        functions=data.get("functions",[])


        for file in files:

            self.graph["nodes"].append({

                "type":"file",
                "name":str(file.get("file",file)) if isinstance(file,dict) else str(file)

            })


        for cls in classes:

            self.graph["nodes"].append({

                "type":"class",
                "name":cls

            })


        for fn in functions:

            self.graph["nodes"].append({

                "type":"function",
                "name":fn

            })


        for cls in classes:

            self.graph["relations"].append({

                "type":"contains",
                "source":"project",
                "target":cls

            })


        for fn in functions:

            self.graph["relations"].append({

                "type":"contains",
                "source":"project",
                "target":fn

            })


        return self.graph



    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )


        output="data/project_relation_graph.json"


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
