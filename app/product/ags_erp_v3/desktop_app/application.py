from .windows.login_window import LoginWindow
from .windows.main_window import MainWindow
from .components.sidebar_menu import SidebarMenu
from .components.dashboard_widgets import DashboardWidgets


class AGSERPV3DesktopApplication:

    def boot(self):

        return {
            "login": LoginWindow().show(),
            "main": MainWindow().show(),
            "menu": SidebarMenu().list(),
            "dashboard": DashboardWidgets().render()
        }
