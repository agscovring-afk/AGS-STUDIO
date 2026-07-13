from app.ui.main_window import MainWindow
import tkinter as tk


def main():
    root = tk.Tk()
    app = MainWindow(root)
    app.mainloop()


if __name__ == "__main__":
    main()
