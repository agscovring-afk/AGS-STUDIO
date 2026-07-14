from datetime import datetime
from .event_bus import event_bus
from .state_manager import state_manager


class AutonomousKernel:

    def __init__(self):
        self.name = "AGS AUTONOMOUS INTELLIGENCE KERNEL"
        self.version = "V2"
        self.started = False


    def start(self):

        self.started = True

        state_manager.set(
            "kernel_status",
            "RUNNING"
        )

        event_bus.emit(
            "KERNEL_STARTED"
        )

        return self.status()


    def stop(self):

        self.started = False

        state_manager.set(
            "kernel_status",
            "STOPPED"
        )

        event_bus.emit(
            "KERNEL_STOPPED"
        )


    def status(self):

        return {
            "name": self.name,
            "version": self.version,
            "running": self.started,
            "state": state_manager.all()
        }


kernel = AutonomousKernel()