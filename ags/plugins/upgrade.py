from ags.version import VersionManager


def register(command_manager):

    command_manager.register(
        "upgrade",
        upgrade
    )


def upgrade(*args):

    if len(args) < 2:

        print(
            "Usage: upgrade module <name>"
        )

        return


    resource = args[0]
    name = args[1]


    if resource == "module":

        vm = VersionManager()

        version = vm.upgrade(name)

        print(
            f"UPGRADED {name} -> {version}"
        )

    else:

        print(
            "Unknown resource"
        )
