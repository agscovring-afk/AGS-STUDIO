import os
import re

from .base_worker import BaseWorker


class FileCreatorWorker(BaseWorker):

    name = "FILE_CREATOR_WORKER"


    def sanitize_path(self, path):

        path = path.replace(
            "/",
            os.sep
        )

        path = path.replace(
            "\\",
            os.sep
        )


        parts = []


        for part in path.split(os.sep):

            part = re.sub(
                r'[<>:"|?*]',
                "_",
                part
            )


            part = part.strip()


            if part:
                parts.append(part)


        return os.sep.join(parts)



    def execute(self, task):

        created = []


        files = task.get(
            "files",
            []
        )


        for file in files:

            original_path = file.get(
                "path"
            )


            path = self.sanitize_path(
                original_path
            )


            content = file.get(
                "content",
                ""
            )


            folder = os.path.dirname(
                path
            )


            if folder:

                os.makedirs(
                    folder,
                    exist_ok=True
                )


            with open(
                path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(content)


            created.append(
                path
            )


        return self.report(
            task,
            {
                "created_files": created,
                "count": len(created)
            }
        )
