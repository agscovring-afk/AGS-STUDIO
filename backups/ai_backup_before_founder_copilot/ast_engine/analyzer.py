import ast
import os
import json


class ASTAnalyzer:

    def __init__(self,root):
        self.root=root
        self.result={
            "project":root,
            "files":[],
            "classes":[],
            "functions":[],
            "imports":[]
        }


    def scan(self):

        for root,dirs,files in os.walk(self.root):

            for file in files:

                if file.endswith(".py"):

                    path=os.path.join(root,file)

                    try:
                        tree=ast.parse(
                            open(path,encoding="utf-8").read()
                        )

                        for node in ast.walk(tree):

                            if isinstance(node,ast.ClassDef):
                                self.result["classes"].append(node.name)

                            if isinstance(node,ast.FunctionDef):
                                self.result["functions"].append(node.name)

                            if isinstance(node,(ast.Import,ast.ImportFrom)):
                                self.result["imports"].append(
                                    type(node).__name__
                                )


                        self.result["files"].append(path)

                    except Exception:
                        pass


        return self.result



    def save(self):

        os.makedirs("data",exist_ok=True)

        with open(
            "data/project_ast.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.result,
                f,
                indent=4
            )


        return "data/project_ast.json"
