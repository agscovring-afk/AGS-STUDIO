from generators.module_generator import ModuleGenerator


def register(command_manager):

    command_manager.register(
        "create",
        create
    )


def create(*args):

    if len(args) < 2:
        print("Usage: create module <name>")
        return


    resource = args[0]

    name = args[1]


    if resource == "module":

        generator = ModuleGenerator()

        generator.generate(name)


    else:

        print(
            f"Unknown resource: {resource}"
        )
