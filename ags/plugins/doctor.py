from pathlib import Path
import json


def register(command_manager):

    command_manager.register(
        "doctor",
        doctor
    )


def doctor(*args):

    print("=== AGS Studio Doctor ===")


    checks = {

        "registry.json":
            Path("registry.json").exists(),

        "schemas":
            Path("schemas").exists(),

        "templates":
            Path("templates").exists(),

        "generators":
            Path("generators").exists(),

        "ags":
            Path("ags").exists(),

    }


    for name, status in checks.items():

        if status:
            print("[ OK ]", name)

        else:
            print("[FAIL]", name)


    if Path("registry.json").exists():

        try:

            data = json.loads(
                Path("registry.json")
                .read_text(
                    encoding="utf-8"
                )
            )

            print(
                "Modules:",
                list(
                    data.get("modules", {})
                    .keys()
                )
            )

        except:

            print(
                "[FAIL] registry format"
            )


    print("Doctor completed")
