from ags.core.agent_manager import AgentManager

from ags.updater.upgrade import UpgradeEngine

from app.ai.generator.module_generator import generate_module
from app.ai.validators.module_validator import validate_module
from app.database.migrations.migration import create_table
from app.metadata.metadata_engine import MetadataEngine
from app.ai.ui_generator.ui_generator import generate_ui

from app.registry.page_registry import save_registry
from app.registry.menu_generator import generate_menu


def register(command_manager):

    command_manager.register(
        "ai",
        ai
    )


def ai(*args):

    if len(args) == 1:

        if args[0] == "upgrade":

            UpgradeEngine().run()

            return

        print("Usage:")
        print("python ags.py ai architect <module>")
        print("python ags.py ai upgrade")

        return


    if len(args) < 2:

        print("Usage:")
        print("python ags.py ai architect <module>")
        print("python ags.py ai upgrade")

        return


    agent = args[0]
    module = args[1]


    manager = AgentManager()

    result = manager.run(
        agent,
        module
    )

    print(result)


    if agent == "architect":

        print("[ARCHITECT] Analysis completed")

        MetadataEngine.create(module)

        generate_ui(module)

        save_registry()

        generate_menu()

        generate_module(module)

        print("[GENERATOR] Module created")

        create_table(module)

        generate_ui(module)

        valid, message = validate_module(module)

        if valid:

            print("[VALIDATOR] MODULE VALID")

        else:

            print("[VALIDATOR ERROR]", message)