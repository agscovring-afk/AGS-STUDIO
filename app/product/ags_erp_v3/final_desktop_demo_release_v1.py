
class FinalDesktopDemoReleaseV1:

    steps = [
        "Start Application",
        "Login",
        "Dashboard",
        "Navigate Modules",
        "Create Business Data",
        "Generate Reports",
        "Backup"
    ]

    def validate(self):
        return self.steps
