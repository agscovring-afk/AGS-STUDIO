
import json,os


class DependencyIntelligenceV2:


    def execute(self,request):

        print("==============================")
        print("AGS DEPENDENCY INTELLIGENCE V2")
        print("==============================")


        with open(
            "data/project_ast.json",
            encoding="utf-8"
        ) as f:

            ast=json.load(f)


        dependencies=[]


        for item in ast.get("imports",[]):

            dependencies.append({
                "import":item
            })


        os.makedirs("data",exist_ok=True)


        with open(
            "data/dependency_map.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                dependencies,
                f,
                indent=4
            )


        impact={

            "total_imports":len(dependencies),

            "affected_components":
            len(ast.get("files",[]))

        }


        with open(
            "data/impact_analysis.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                impact,
                f,
                indent=4
            )


        return {

            "engine":
            "AGS DEPENDENCY INTELLIGENCE V2",

            "status":
            "COMPLETED",

            "imports":
            len(dependencies),

            "impact":
            impact,

            "outputs":[
                "data/dependency_map.json",
                "data/impact_analysis.json"
            ]

        }


bridge=DependencyIntelligenceV2()
