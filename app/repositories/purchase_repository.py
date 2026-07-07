import sqlite3
from typing import Optional, List
from datetime import datetime
from app.models.purchase import Purchase
from app.models.purchase_line import PurchaseLine


class PurchaseRepository:
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
                CREATE TABLE IF NOT EXISTS purchases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    code TEXT UNIQUE,
                    supplier_id INTEGER,
                    date TEXT,
                    status TEXT,
                    total REAL,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS purchase_lines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    purchase_id INTEGER,
                    line_no INTEGER,
                    item_type TEXT,
                    item_id INTEGER,
                    description TEXT,
                    quantity REAL,
                    unit_price REAL,
                    total REAL,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY(purchase_id) REFERENCES purchases(id) ON DELETE CASCADE
                )
                """
            )

    def add_purchase(self, p: Purchase) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO purchases (company_id, code, supplier_id, date, status, total, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (p.company_id, p.code, p.supplier_id, p.date, p.status, p.total, p.created_at.isoformat(), p.updated_at.isoformat()),
            )
            return cur.lastrowid

    def add_line(self, line: PurchaseLine) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO purchase_lines (purchase_id, line_no, item_type, item_id, description, quantity, unit_price, total, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (line.purchase_id, line.line_no, line.item_type, line.item_id, line.description, line.quantity, line.unit_price, line.total, line.created_at.isoformat(), line.updated_at.isoformat()),
            )
            return cur.lastrowid

    def get_purchase(self, purchase_id: int) -> Optional[Purchase]:
        with self._conn() as c:
            r = c.execute("SELECT * FROM purchases WHERE id = ?", (purchase_id,)).fetchone()
            if not r:
                return None
            return Purchase(id=r['id'], company_id=r['company_id'], code=r['code'], supplier_id=r['supplier_id'], date=r['date'], status=r['status'], total=r['total'])

    def list_purchases_by_supplier(self, supplier_id: int) -> List[Purchase]:
        with self._conn() as c:
            rows = c.execute("SELECT * FROM purchases WHERE supplier_id = ? ORDER BY id", (supplier_id,)).fetchall()
            return [Purchase(id=r['id'], company_id=r['company_id'], code=r['code'], supplier_id=r['supplier_id'], date=r['date'], status=r['status'], total=r['total']) for r in rows]
