from pathlib import Path
import json


class ModuleGenerator:


    def __init__(self):

        from app.ai.self_developer.compiler.runner import CompilerRunner

        self.compiler = CompilerRunner()



    def create(self,module):


        print(
            f"[AGS AI] Creating module: {module}"
        )


        base = Path(
            "generated/modules"
        ) / module


        folders = [

            "models",
            "repositories",
            "services",
            "controllers",
            "database",
            "tests",
            "metadata"

        ]


        for folder in folders:

            (base / folder).mkdir(
                parents=True,
                exist_ok=True
            )


        metadata = {

            "module": module,

            "version": "1.0.0",

            "generated_by": "AGS-STUDIO AI"

        }


        (base / "metadata" / "module.json").write_text(

            json.dumps(
                metadata,
                indent=4
            ),

            encoding="utf8"

        )


        # temporary generation layer

        files = {

            f"models/{module}.py":
f'''class {module.title().replace("_","")}:
    pass
''',

            f"services/{module}_service.py":
f'''class {module.title().replace("_","")}Service:
    pass
''',

            f"controllers/{module}_controller.py":
f'''class {module.title().replace("_","")}Controller:
    pass
'''

        }


        for file,content in files.items():

            (base / file).write_text(
                content,
                encoding="utf8"
            )



        result = self.compiler.run(
            str(base)
        )


        return {

            "status":"success",

            "module":module,

            "path":str(base),

            "compiler":result

        }
