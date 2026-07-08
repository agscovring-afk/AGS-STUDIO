import os
import importlib


def validate_module(module):

    required = [

        f"app/models/{module}.py",
        f"app/repositories/{module}_repository.py",
        f"app/services/{module}_service.py",
        f"app/controllers/{module}_controller.py"

    ]


    for file in required:

        if not os.path.exists(file):

            return False, f"Missing: {file}"


    try:

        importlib.import_module(
            f"app.models.{module}"
        )

    except Exception as e:

        return False, str(e)


    return True, "MODULE VALID"
