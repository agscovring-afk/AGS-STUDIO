"""
AGS Autonomous V2 Entry Point
"""

from .runner import AutonomousRunner


def start(context):

    runner = AutonomousRunner(
        context
    )

    return runner.run()