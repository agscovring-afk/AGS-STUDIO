class CodeExecutor:


    def execute(self, code):

        try:

            exec(code)

            return {
                "status":"EXECUTED"
            }


        except Exception as e:

            return {
                "status":"FAILED",
                "error":str(e)
            }


executor = CodeExecutor()
