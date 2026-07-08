from ags.core.agent_manager import AgentManager

from ags.updater.upgrade import UpgradeEngine

from app.ai.generator.module_generator import generate_module
from app.ai.validators.module_validator import validate_module
from app.database.migrations.migration import create_table
from app.metadata.metadata_engine import MetadataEngine
from app.ai.ui_generator.ui_generator import generate_ui

from app.registry.page_registry import save_registry
from app.registry.menu_generator import generate_menu



def generate_fields(module):

    common = {

        "customers": [
            {
                "name": "id",
                "type": "INTEGER",
                "primary_key": True
            },
            {
                "name": "name",
                "type": "TEXT"
            },
            {
                "name": "phone",
                "type": "TEXT"
            },
            {
                "name": "email",
                "type": "TEXT"
            },
            {
                "name": "address",
                "type": "TEXT"
            }
        ],


        "products": [
            {
                "name": "id",
                "type": "INTEGER",
                "primary_key": True
            },
            {
                "name": "name",
                "type": "TEXT"
            },
            {
                "name": "reference",
                "type": "TEXT"
            },
            {
                "name": "price",
                "type": "REAL"
            },
            {
                "name": "quantity",
                "type": "INTEGER"
            }
        ],


        "invoices": [
            {
                "name": "id",
                "type": "INTEGER",
                "primary_key": True
            },
            {
                "name": "customer_id",
                "type": "INTEGER"
            },
            {
                "name": "date",
                "type": "TEXT"
            },
            {
                "name": "total",
                "type": "REAL"
            },
            {
                "name": "status",
                "type": "TEXT"
            }
        ]

    }


    return common.get(
        module,
        [
            {
                "name": "id",
                "type": "INTEGER",
                "primary_key": True
            },
            {
                "name": "name",
                "type": "TEXT"
            }
        ]
    )



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


        MetadataEngine.create(
            module,
            generate_fields(module)
        )


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

            print(
                "[VALIDATOR ERROR]",
                message
            )