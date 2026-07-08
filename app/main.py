"""
AGS ERP V2
Application Entry Point
"""

from app.ui.main_window import MainWindow


def main():

    app = MainWindow()

    app.mainloop()


if __name__ == "__main__":
    main()
