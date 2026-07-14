import ast


class SyntaxValidator:


    def validate(self, path):

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                ast.parse(
                    f.read()
                )


            return {
                "valid": True,
                "file": path
            }


        except Exception as e:

            return {
                "valid": False,
                "file": path,
                "error": str(e)
            }



validator = SyntaxValidator()
