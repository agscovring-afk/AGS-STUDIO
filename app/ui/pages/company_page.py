"""Simple Company management page (minimal CRUD UI)."""
try:
    import customtkinter as ctk
except Exception:
    ctk = None

import tkinter as tk
from app.controllers.company_controller import CompanyController
from app.repositories.company_repository import CompanyRepository
import os


class CompanyPage:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.join(os.getcwd(), "ags_erp.db")
        self.repo = CompanyRepository(self.db_path)
        self.controller = CompanyController(self.repo)
        self.controller.init_db()

    def show(self):
        if ctk:
            self._show_ctk()
        else:
            self._show_tk()

    def _show_ctk(self):
        app = ctk.CTk()
        app.title("Companies — AGS ERP V2")
        app.geometry("480x220")

        lbl1 = ctk.CTkLabel(app, text="Legal name")
        lbl1.pack(padx=8, pady=4)
        e1 = ctk.CTkEntry(app)
        e1.pack(fill="x", padx=8)

        lbl2 = ctk.CTkLabel(app, text="Commercial name")
        lbl2.pack(padx=8, pady=4)
        e2 = ctk.CTkEntry(app)
        e2.pack(fill="x", padx=8)

        def on_create():
            legal = e1.get()
            comm = e2.get()
            cid = self.controller.create_company(legal, comm, "COM-00001", "DZD", "fr")
            ctk.CTkLabel(app, text=f"Created company id={cid}").pack(pady=6)

        btn = ctk.CTkButton(app, text="Create", command=on_create)
        btn.pack(pady=12)
        app.mainloop()

    def _show_tk(self):
        root = tk.Tk()
        root.title("Companies — AGS ERP V2 (tk)")

        tk.Label(root, text="Legal name").pack(padx=8, pady=4)
        e1 = tk.Entry(root)
        e1.pack(fill="x", padx=8)

        tk.Label(root, text="Commercial name").pack(padx=8, pady=4)
        e2 = tk.Entry(root)
        e2.pack(fill="x", padx=8)

        def on_create():
            legal = e1.get()
            comm = e2.get()
            cid = self.controller.create_company(legal, comm, "COM-00001", "DZD", "fr")
            tk.Label(root, text=f"Created company id={cid}").pack(pady=6)

        tk.Button(root, text="Create", command=on_create).pack(pady=12)
        root.mainloop()


if __name__ == "__main__":
    CompanyPage().show()
