
import traceback


class ProductionGuard:


    def safe_execute(self, func, *args, **kwargs):

        try:

            return {

                "status": "success",
                "result": func(*args, **kwargs)

            }


        except Exception as e:

            return {

                "status": "error",
                "error": str(e),
                "trace": traceback.format_exc()

            }



production_guard = ProductionGuard()
