import ast
from pathlib import Path


class CodeValidator:


    def validate_file(self,file):

        path = Path(file)

        try:

            ast.parse(
                path.read_text(
                    encoding="utf8"
                )
            )

            return {
                "file":str(path),
                "status":"success"
            }


        except Exception as e:

            return {
                "file":str(path),
                "status":"error",
                "error":str(e)
            }


    def validate_folder(self,folder):

        results=[]

        for file in Path(folder).rglob("*.py"):

            results.append(
                self.validate_file(file)
            )


        return results
