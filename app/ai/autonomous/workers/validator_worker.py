from .base_worker import BaseWorker


class ValidatorWorker(BaseWorker):

    name = "VALIDATOR_WORKER"


    def execute(self, task):

        files = task.get(
            "files",
            []
        )


        errors = []


        for file in files:

            if not file.endswith(".py"):

                errors.append(
                    file
                )


        return self.report(
            task,
            {
                "valid":
                len(errors)==0,

                "errors":
                errors
            }
        )
