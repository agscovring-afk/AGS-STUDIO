
import tkinter as tk

from app.ui.main_window import MainWindow


def main():

    root = tk.Tk()

    root.title("AGS-STUDIO ERP Platform")

    root.geometry("1200x700")

    root.minsize(
        900,
        600
    )

    app = MainWindow(root)

    app.mainloop()


if __name__ == "__main__":
    main()
