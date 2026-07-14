"""
AGS Autonomous AI Package
Lazy Initialization
"""

__all__ = [
    "AutonomousController",
    "AutonomousService",
    "AutonomousMonitor",
    "AutonomousMemory",
    "AutonomousKnowledge",
]


def __getattr__(name):

    if name == "AutonomousController":
        from .controller import AutonomousController
        return AutonomousController

    if name == "AutonomousService":
        from .service import AutonomousService
        return AutonomousService

    if name == "AutonomousMonitor":
        from .monitor import AutonomousMonitor
        return AutonomousMonitor

    if name == "AutonomousMemory":
        from .memory import AutonomousMemory
        return AutonomousMemory

    if name == "AutonomousKnowledge":
        from .knowledge import AutonomousKnowledge
        return AutonomousKnowledge

    raise AttributeError(
        f"module app.ai.autonomous has no attribute {name}"
    )
