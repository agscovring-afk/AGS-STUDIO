from app.ai.autonomous.workers.bridge import bridge


class ERPBuildExecutor:


    def execute(self, modules):

        results = []


        for module in modules:

            result = bridge.dispatch(
                "module_builder",
                {
                    "module":
                    f"erp/{module}"
                }
            )

            results.append(result)


        return {
            "executor":
            "ERP AUTO BUILD EXECUTOR V1",

            "modules":
            len(results),

            "results":
            results
        }



executor = ERPBuildExecutor()
