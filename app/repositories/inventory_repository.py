import sqlite3
from typing import Optional, List
from datetime import datetime
from app.models.warehouse import Warehouse
from app.models.stock_movement import StockMovement
from app.models.stock_level import StockLevel


class InventoryRepository:
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
                CREATE TABLE IF NOT EXISTS warehouses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    name TEXT,
                    location TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS stock_levels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    warehouse_id INTEGER,
                    quantity REAL DEFAULT 0,
                    reserved REAL DEFAULT 0,
                    created_at TEXT,
                    updated_at TEXT,
                    UNIQUE(product_id, warehouse_id)
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS stock_movements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    warehouse_from INTEGER,
                    warehouse_to INTEGER,
                    movement_type TEXT,
                    quantity REAL,
                    reference TEXT,
                    reason TEXT,
                    created_at TEXT
                )
                """
            )

    # Warehouses
    def add_warehouse(self, w: Warehouse) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO warehouses (company_id, name, location, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (w.company_id, w.name, w.location, w.created_at.isoformat(), w.updated_at.isoformat()),
            )
            return cur.lastrowid

    def list_warehouses(self) -> List[Warehouse]:
        with self._conn() as c:
            rows = c.execute("SELECT * FROM warehouses ORDER BY id").fetchall()
            return [Warehouse(id=r['id'], company_id=r['company_id'], name=r['name'], location=r['location']) for r in rows]

    # Stock levels and movements (transactional)
    def record_movement(self, sm: StockMovement) -> int:
        with self._conn() as c:
            try:
                c.execute('BEGIN')
                # insert movement record
                cur = c.execute(
                    "INSERT INTO stock_movements (product_id, warehouse_from, warehouse_to, movement_type, quantity, reference, reason, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (sm.product_id, sm.warehouse_from, sm.warehouse_to, sm.movement_type, sm.quantity, sm.reference, sm.reason, sm.created_at.isoformat()),
                )
                mid = cur.lastrowid

                # update stock levels based on movement type
                if sm.movement_type == 'IN':
                    self._add_quantity(c, sm.product_id, sm.warehouse_to, sm.quantity)
                elif sm.movement_type == 'OUT':
                    self._add_quantity(c, sm.product_id, sm.warehouse_from, -sm.quantity)
                elif sm.movement_type == 'TRANSFER':
                    self._add_quantity(c, sm.product_id, sm.warehouse_from, -sm.quantity)
                    self._add_quantity(c, sm.product_id, sm.warehouse_to, sm.quantity)
                elif sm.movement_type == 'ADJUSTMENT':
                    # adjustment: warehouse_to used as target warehouse, positive or negative quantity
                    self._add_quantity(c, sm.product_id, sm.warehouse_to, sm.quantity)
                else:
                    raise ValueError('Unknown movement type')

                c.execute('COMMIT')
                return mid
            except Exception:
                c.execute('ROLLBACK')
                raise

    def _add_quantity(self, conn, product_id: int, warehouse_id: int, delta: float):
        # helper that updates or inserts stock_levels
        row = conn.execute("SELECT id, quantity FROM stock_levels WHERE product_id = ? AND warehouse_id = ?", (product_id, warehouse_id)).fetchone()
        now = datetime.utcnow().isoformat()
        if row:
            new_q = row['quantity'] + delta
            conn.execute("UPDATE stock_levels SET quantity = ?, updated_at = ? WHERE id = ?", (new_q, now, row['id']))
        else:
            conn.execute("INSERT INTO stock_levels (product_id, warehouse_id, quantity, reserved, created_at, updated_at) VALUES (?, ?, ?, 0, ?, ?)", (product_id, warehouse_id, max(0.0, delta), now, now))

    def get_stock_level(self, product_id: int, warehouse_id: int) -> Optional[StockLevel]:
        with self._conn() as c:
            r = c.execute("SELECT * FROM stock_levels WHERE product_id = ? AND warehouse_id = ?", (product_id, warehouse_id)).fetchone()
            if not r:
                return None
            return StockLevel(id=r['id'], product_id=r['product_id'], warehouse_id=r['warehouse_id'], quantity=r['quantity'], reserved=r['reserved'])

    def list_movements(self, product_id: int = None) -> List[StockMovement]:
        with self._conn() as c:
            if product_id:
                rows = c.execute("SELECT * FROM stock_movements WHERE product_id = ? ORDER BY created_at", (product_id,)).fetchall()
            else:
                rows = c.execute("SELECT * FROM stock_movements ORDER BY created_at").fetchall()
            results = []
            for r in rows:
                results.append(StockMovement(id=r['id'], product_id=r['product_id'], warehouse_from=r['warehouse_from'], warehouse_to=r['warehouse_to'], movement_type=r['movement_type'], quantity=r['quantity'], reference=r['reference'], reason=r['reason']))
            return results
