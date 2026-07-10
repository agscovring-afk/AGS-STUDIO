import sqlite3
from typing import List, Optional
from datetime import datetime
from app.models.boq import BOQ
from app.models.boq_line import BOQLine


class BOQRepository:
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
                CREATE TABLE IF NOT EXISTS boq (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    code TEXT UNIQUE,
                    title TEXT,
                    description TEXT,
                    revision INTEGER DEFAULT 1,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS boq_lines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    boq_id INTEGER,
                    line_no INTEGER,
                    item_type TEXT,
                    item_id INTEGER,
                    description TEXT,
                    quantity REAL,
                    unit_id INTEGER,
                    unit_price REAL,
                    total REAL,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY(boq_id) REFERENCES boq(id) ON DELETE CASCADE
                )
                """
            )

    def add_boq(self, b: BOQ) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO boq (project_id, code, title, description, revision, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (b.project_id, b.code, b.title, b.description, b.revision, b.created_at.isoformat(), b.updated_at.isoformat()),
            )
            return cur.lastrowid

    def add_line(self, line: BOQLine) -> int:
        with self._conn() as c:
            cur = c.execute(
                """
                INSERT INTO boq_lines (boq_id, line_no, item_type, item_id, description, quantity, unit_id, unit_price, total, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    line.boq_id,
                    line.line_no,
                    line.item_type,
                    line.item_id,
                    line.description,
                    line.quantity,
                    line.unit_id,
                    line.unit_price,
                    line.total,
                    line.created_at.isoformat(),
                    line.updated_at.isoformat(),
                ),
            )
            return cur.lastrowid

    def list_boqs_for_project(self, project_id: int) -> List[BOQ]:
        with self._conn() as c:
            rows = c.execute("SELECT * FROM boq WHERE project_id = ? ORDER BY id", (project_id,)).fetchall()
            results = []
            for r in rows:
                results.append(BOQ(id=r['id'], project_id=r['project_id'], code=r['code'], title=r['title'], description=r['description'], revision=r['revision']))
            return results

    def get_lines(self, boq_id: int) -> List[BOQLine]:
        with self._conn() as c:
            rows = c.execute("SELECT * FROM boq_lines WHERE boq_id = ? ORDER BY line_no", (boq_id,)).fetchall()
            return [BOQLine(id=r['id'], boq_id=r['boq_id'], line_no=r['line_no'], item_type=r['item_type'], item_id=r['item_id'], description=r['description'], quantity=r['quantity'], unit_id=r['unit_id'], unit_price=r['unit_price'], total=r['total']) for r in rows]
