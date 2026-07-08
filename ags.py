import sys
import tkinter as tk

from ags.core.engine import AGSEngine
from ags.core.command_manager import CommandManager

from ags.plugins import create
from ags.plugins import upgrade
from ags.plugins import doctor
from ags.plugins import validate
from ags.plugins import ai
from ags.plugins import team
from ags.plugins import build
from ags.plugins import help

from app.ui.main_window import MainWindow


def main():

    engine = AGSEngine()

    command_manager = CommandManager()

    create.register(command_manager)
    upgrade.register(command_manager)
    doctor.register(command_manager)
    validate.register(command_manager)
    ai.register(command_manager)
    team.register(command_manager)
    build.register(command_manager)
    help.register(command_manager)

    if len(sys.argv) > 1:

        command_manager.execute(
            sys.argv[1],
            *sys.argv[2:]
        )

    else:

        root = tk.Tk()

        root.title(
            "AGS-STUDIO ERP"
        )

        root.geometry(
            "1200x700"
        )

        MainWindow(root)

        root.mainloop()


if __name__ == "__main__":
    main()