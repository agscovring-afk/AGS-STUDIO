from ags.core.agent_manager import AgentManager
from ags.core.ai_orchestrator import AIOrchestrator
from generators.module_generator import ModuleGenerator
from ags.registry import Registry


def register(command_manager):

    command_manager.register(
        "build",
        build
    )


def build(*args):

    if len(args) < 1:

        print(
            "Usage: build <module>"
        )

        return


    module = args[0]


    print("=== AGS BUILD ENGINE ===")


    print()

    manager = AgentManager()

    orchestrator = AIOrchestrator(
        manager
    )


    report = orchestrator.run_team(
        module
    )


    print()

    print("Generating Module...")


    generator = ModuleGenerator()

    generator.generate(
        module
    )


    print()

    print("Registering...")


    registry = Registry()

    registry.register(
        module
    )


    print()

    print("BUILD COMPLETED")


    return report
