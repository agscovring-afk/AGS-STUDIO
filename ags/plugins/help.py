def register(command_manager):

    command_manager.register(
        "help",
        help_command
    )


def help_command(*args):

    print("""
===================================
 AGS-STUDIO COMMAND CENTER
===================================

AI:
 python ags.py ai upgrade
 python ags.py ai architect <module>

SYSTEM:
 python ags.py doctor
 python ags.py validate

BUILD:
 python ags.py build

TEAM:
 python ags.py team

CREATE:
 python ags.py create

===================================
""")
