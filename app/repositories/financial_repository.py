import sqlite3
from typing import Optional, List
from datetime import datetime
from app.models.quotation import Quotation
from app.models.quotation_line import QuotationLine
from app.models.invoice import Invoice
from app.models.invoice_line import InvoiceLine
from app.models.payment import Payment


class FinancialRepository:
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
                CREATE TABLE IF NOT EXISTS numbering_sequences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    prefix TEXT,
                    year INTEGER,
                    last_number INTEGER,
                    reset_period TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS quotations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    code TEXT UNIQUE,
                    client_id INTEGER,
                    project_id INTEGER,
                    date TEXT,
                    validity_date TEXT,
                    status TEXT,
                    subtotal REAL,
                    tax REAL,
                    total REAL,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS quotation_lines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quotation_id INTEGER,
                    line_no INTEGER,
                    item_type TEXT,
                    item_id INTEGER,
                    description TEXT,
                    quantity REAL,
                    unit_price REAL,
                    total REAL,
                    FOREIGN KEY(quotation_id) REFERENCES quotations(id) ON DELETE CASCADE
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    code TEXT UNIQUE,
                    client_id INTEGER,
                    project_id INTEGER,
                    date TEXT,
                    due_date TEXT,
                    status TEXT,
                    subtotal REAL,
                    tax REAL,
                    total REAL,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS invoice_lines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER,
                    line_no INTEGER,
                    item_type TEXT,
                    item_id INTEGER,
                    description TEXT,
                    quantity REAL,
                    unit_price REAL,
                    total REAL,
                    FOREIGN KEY(invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER,
                    amount REAL,
                    date TEXT,
                    method TEXT,
                    reference TEXT,
                    created_at TEXT,
                    FOREIGN KEY(invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
                )
                """
            )

    # Numbering
    def get_next_number(self, company_id: int, prefix: str, year: int) -> str:
        with self._conn() as c:
            row = c.execute("SELECT id, last_number FROM numbering_sequences WHERE company_id = ? AND prefix = ? AND year = ?", (company_id, prefix, year)).fetchone()
            if row:
                next_num = row["last_number"] + 1
                c.execute("UPDATE numbering_sequences SET last_number = ? WHERE id = ?", (next_num, row["id"]))
            else:
                next_num = 1
                c.execute("INSERT INTO numbering_sequences (company_id, prefix, year, last_number, reset_period) VALUES (?, ?, ?, ?, ?)", (company_id, prefix, year, next_num, 'yearly'))
            return f"{prefix}-{year}-{next_num:05d}"

    # Quotations
    def add_quotation(self, q: Quotation) -> int:
        with self._conn() as c:
            cur = c.execute(
                """
                INSERT INTO quotations (company_id, code, client_id, project_id, date, validity_date, status, subtotal, tax, total, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (q.company_id, q.code, q.client_id, q.project_id, q.date, q.validity_date, q.status, q.subtotal, q.tax, q.total, q.created_at.isoformat(), q.updated_at.isoformat()),
            )
            return cur.lastrowid

    def add_quotation_line(self, line: QuotationLine) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO quotation_lines (quotation_id, line_no, item_type, item_id, description, quantity, unit_price, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (line.quotation_id, line.line_no, line.item_type, line.item_id, line.description, line.quantity, line.unit_price, line.total),
            )
            return cur.lastrowid

    # Invoices
    def add_invoice(self, inv: Invoice) -> int:
        with self._conn() as c:
            cur = c.execute(
                """
                INSERT INTO invoices (company_id, code, client_id, project_id, date, due_date, status, subtotal, tax, total, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (inv.company_id, inv.code, inv.client_id, inv.project_id, inv.date, inv.due_date, inv.status, inv.subtotal, inv.tax, inv.total, inv.created_at.isoformat(), inv.updated_at.isoformat()),
            )
            return cur.lastrowid

    def add_invoice_line(self, line: InvoiceLine) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO invoice_lines (invoice_id, line_no, item_type, item_id, description, quantity, unit_price, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (line.invoice_id, line.line_no, line.item_type, line.item_id, line.description, line.quantity, line.unit_price, line.total),
            )
            return cur.lastrowid

    # Payments
    def add_payment(self, p: Payment) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO payments (invoice_id, amount, date, method, reference, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (p.invoice_id, p.amount, p.date, p.method, p.reference, p.created_at.isoformat()),
            )
            return cur.lastrowid
