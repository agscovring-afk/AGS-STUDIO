from .base_worker import BaseWorker


class ScannerWorker(BaseWorker):

    name = "SCANNER_WORKER"


    def execute(self, task):

        path = task.get(
            "path",
            "generated"
        )


        import os


        files = []


        for root,dirs,names in os.walk(path):

            for name in names:

                files.append(
                    os.path.join(
                        root,
                        name
                    )
                )


        return self.report(
            task,
            {
                "files":
                files,

                "count":
                len(files)
            }
        )
