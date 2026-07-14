import os
import re

from .base_worker import BaseWorker


class FileCreatorWorker(BaseWorker):

    name = "FILE_CREATOR_WORKER"


    def sanitize_path(self, path):

        invalid_chars = r'[<>:"/\\|?*]'

        parts = path.split(os.sep)

        clean_parts = []

        for part in parts:

            part = re.sub(invalid_chars, "_", part)

            part = part.strip()

            if part:
                clean_parts.append(part)

        return os.sep.join(clean_parts)


    def execute(self, task):

        created = []

        files = task.get("files", [])


        for file in files:

            original_path = file.get("path")

            path = self.sanitize_path(original_path)

            content = file.get("content", "")


            folder = os.path.dirname(path)


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


            created.append(path)


        return self.report(
            task,
            {
                "created_files": created,
                "count": len(created)
            }
        )