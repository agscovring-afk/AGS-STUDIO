import os


class PathValidator:


    def validate(self, path):

        folder = os.path.dirname(path)


        if folder:

            os.makedirs(
                folder,
                exist_ok=True
            )


        return True



path_validator = PathValidator()
