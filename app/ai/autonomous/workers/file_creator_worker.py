import os

from .base_worker import BaseWorker


class FileCreatorWorker(BaseWorker):

    name = "FILE_CREATOR_WORKER"


    def execute(self, task):

        created = []

        files = task.get("files", [])

        for file in files:

            path = file.get("path")
            content = file.get("content", "")

            folder = os.path.dirname(path)

            if folder:
                os.makedirs(folder, exist_ok=True)


            with open(
                path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(content)


            created.append(path)


        return self.report(
            task,
            {
                "created_files": created,
                "count": len(created)
            }
        )
