from ags.core.agent_manager import AgentManager


def register(command_manager):

    command_manager.register(
        "team",
        team
    )


def team(*args):

    if len(args) < 1:

        print(
            "Usage: team <module>"
        )

        return


    module = args[0]


    manager = AgentManager()


    agents = [

        "architect",
        "backend",
        "database",
        "ui",
        "testing",
        "documentation"

    ]


    print("=== AGS AI TEAM ===")


    for agent in agents:

        print()
        print(
            "Agent:",
            agent
        )

        result = manager.run(
            agent,
            module
        )

        print(result)


    print()
    print("Team analysis completed")
