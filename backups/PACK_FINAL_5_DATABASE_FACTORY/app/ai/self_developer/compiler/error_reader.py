import traceback


class ErrorReader:


    def read(self, error):

        if isinstance(error, Exception):

            return {
                "type": error.__class__.__name__,
                "message": str(error),
                "trace": traceback.format_exc()
            }


        return {
            "type": "RuntimeError",
            "message": str(error),
            "trace": ""
        }


    def format(self, error):

        data = self.read(error)

        return f"""
ERROR TYPE:
{data['type']}

MESSAGE:
{data['message']}

TRACE:
{data['trace']}
"""
