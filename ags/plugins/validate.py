from pathlib import Path
from ags.registry import Registry


def register(command_manager):

    command_manager.register(
        "validate",
        validate
    )


def validate(*args):

    print("=== AGS Validator ===")


    registry = Registry()

    modules = registry.list()


    for module in modules:

        print()
        print("Checking:", module)


        files = [

            f"app/models/{module}.py",

            f"app/repositories/{module}_repository.py",

            f"app/services/{module}_service.py",

            f"app/controllers/{module}_controller.py",

            f"app/ui/pages/{module}_page.py",

            f"app/ui/dialogs/{module}_dialog.py",

        ]


        for file in files:

            if Path(file).exists():

                print("[ OK ]", file)

            else:

                print("[FAIL]", file)


    print()
    print("Validation completed")
