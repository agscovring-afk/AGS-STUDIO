import os


class FileGenerator:


    def create(self, path, content):

        try:

            os.makedirs(
                os.path.dirname(path),
                exist_ok=True
            )

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(content)


            return {
                "status":"CREATED",
                "file":path
            }


        except Exception as e:

            return {
                "status":"ERROR",
                "error":str(e)
            }


generator = FileGenerator()
