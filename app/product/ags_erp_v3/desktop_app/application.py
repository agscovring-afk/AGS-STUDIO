import tkinter as tk

from .windows.main_window import MainWindow


class AGSERPV3DesktopApplication:

    def __init__(self):
        self.root = tk.Tk()
        self.window = MainWindow(self.root)

    def start(self):

        print("=" * 60)
        print(" AGS ERP V3 DESKTOP GUI RUNTIME ")
        print("=" * 60)

        print("AGS ERP V3 MAIN WINDOW LOADED")

        self.root.mainloop()


def main():

    app = AGSERPV3DesktopApplication()
    app.start()


if __name__ == "__main__":
    main()
