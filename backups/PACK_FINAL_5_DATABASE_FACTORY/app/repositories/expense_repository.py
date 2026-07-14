import sqlite3
from typing import Optional, List
from datetime import datetime
from app.models.expense import Expense
from app.models.expense_category import ExpenseCategory


class ExpenseRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def create_tables(self):
        with self._conn() as c:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS expense_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    name TEXT,
                    description TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    category_id INTEGER,
                    amount REAL,
                    date TEXT,
                    project_id INTEGER,
                    supplier_id INTEGER,
                    payment_method TEXT,
                    attachment TEXT,
                    notes TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY(category_id) REFERENCES expense_categories(id)
                )
                """
            )

    def add_category(self, cat: ExpenseCategory) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO expense_categories (company_id, name, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (cat.company_id, cat.name, cat.description, cat.created_at.isoformat(), cat.updated_at.isoformat()),
            )
            return cur.lastrowid

    def add_expense(self, e: Expense) -> int:
        with self._conn() as c:
            cur = c.execute(
                """
                INSERT INTO expenses (company_id, category_id, amount, date, project_id, supplier_id, payment_method, attachment, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (e.company_id, e.category_id, e.amount, e.date, e.project_id, e.supplier_id, e.payment_method, e.attachment, e.notes, e.created_at.isoformat(), e.updated_at.isoformat()),
            )
            return cur.lastrowid

    def get_expense(self, expense_id: int) -> Optional[Expense]:
        with self._conn() as c:
            r = c.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
            if not r:
                return None
            return Expense(id=r['id'], company_id=r['company_id'], category_id=r['category_id'], amount=r['amount'], date=r['date'], project_id=r['project_id'], supplier_id=r['supplier_id'], payment_method=r['payment_method'], attachment=r['attachment'], notes=r['notes'])

    def list_expenses_by_project(self, project_id: int) -> List[Expense]:
        with self._conn() as c:
            rows = c.execute("SELECT * FROM expenses WHERE project_id = ? ORDER BY id", (project_id,)).fetchall()
            return [Expense(id=r['id'], company_id=r['company_id'], category_id=r['category_id'], amount=r['amount'], date=r['date'], project_id=r['project_id'], supplier_id=r['supplier_id'], payment_method=r['payment_method'], attachment=r['attachment'], notes=r['notes']) for r in rows]
