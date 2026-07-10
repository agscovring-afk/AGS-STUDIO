from agents.master import MasterAgent


def register(command_manager):

    command_manager.register(
        "ask",
        ask
    )


def ask(*args):

    if len(args) < 1:

        print(
            "Usage: ask <request>"
        )

        return


    request = " ".join(args)

    print("=== AGS MASTER AI ===")

    master = MasterAgent()

    result = master.ask(
        request
    )

    print()

    print(result)

    print()

    print("MASTER COMPLETED")

    return result
