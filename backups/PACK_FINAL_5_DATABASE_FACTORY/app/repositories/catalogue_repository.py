import sqlite3
from datetime import datetime
from typing import List, Optional
from app.models.category import Category
from app.models.unit import Unit
from app.models.product import Product
from app.models.service import Service


class CatalogueRepository:
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
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    name TEXT,
                    parent_id INTEGER,
                    description TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS units (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    symbol TEXT,
                    conversion_factor REAL,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    code TEXT UNIQUE,
                    name TEXT,
                    category_id INTEGER,
                    unit_id INTEGER,
                    cost_price REAL,
                    sale_price REAL,
                    tax_rate REAL,
                    stock_tracked INTEGER DEFAULT 0,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY(category_id) REFERENCES categories(id),
                    FOREIGN KEY(unit_id) REFERENCES units(id)
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    code TEXT UNIQUE,
                    name TEXT,
                    category_id INTEGER,
                    unit_id INTEGER,
                    default_price REAL,
                    tax_rate REAL,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY(category_id) REFERENCES categories(id),
                    FOREIGN KEY(unit_id) REFERENCES units(id)
                )
                """
            )

    # Categories
    def add_category(self, cat: Category) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO categories (company_id, name, parent_id, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (cat.company_id, cat.name, cat.parent_id, cat.description, cat.created_at.isoformat(), cat.updated_at.isoformat()),
            )
            return cur.lastrowid

    def list_categories(self) -> List[Category]:
        with self._conn() as c:
            rows = c.execute("SELECT * FROM categories ORDER BY id").fetchall()
            return [Category(id=r['id'], company_id=r['company_id'], name=r['name'], parent_id=r['parent_id'], description=r['description']) for r in rows]

    # Units
    def add_unit(self, unit: Unit) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO units (name, symbol, conversion_factor, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (unit.name, unit.symbol, unit.conversion_factor, unit.created_at.isoformat(), unit.updated_at.isoformat()),
            )
            return cur.lastrowid

    def list_units(self) -> List[Unit]:
        with self._conn() as c:
            rows = c.execute("SELECT * FROM units ORDER BY id").fetchall()
            return [Unit(id=r['id'], name=r['name'], symbol=r['symbol'], conversion_factor=r['conversion_factor']) for r in rows]

    # Products
    def add_product(self, p: Product) -> int:
        with self._conn() as c:
            cur = c.execute(
                """
                INSERT INTO products (company_id, code, name, category_id, unit_id, cost_price, sale_price, tax_rate, stock_tracked, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (p.company_id, p.code, p.name, p.category_id, p.unit_id, p.cost_price, p.sale_price, p.tax_rate, 1 if p.stock_tracked else 0, p.created_at.isoformat(), p.updated_at.isoformat()),
            )
            return cur.lastrowid

    def get_product(self, product_id: int) -> Optional[Product]:
        with self._conn() as c:
            r = c.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            if not r:
                return None
            return Product(id=r['id'], company_id=r['company_id'], code=r['code'], name=r['name'], category_id=r['category_id'], unit_id=r['unit_id'], cost_price=r['cost_price'], sale_price=r['sale_price'], tax_rate=r['tax_rate'], stock_tracked=bool(r['stock_tracked']))

    def search_products(self, term: str) -> List[Product]:
        with self._conn() as c:
            rows = c.execute("SELECT * FROM products WHERE name LIKE ? OR code LIKE ? ORDER BY id", (f"%{term}%", f"%{term}%")).fetchall()
            return [Product(id=r['id'], company_id=r['company_id'], code=r['code'], name=r['name'], category_id=r['category_id'], unit_id=r['unit_id'], cost_price=r['cost_price'], sale_price=r['sale_price'], tax_rate=r['tax_rate'], stock_tracked=bool(r['stock_tracked'])) for r in rows]

    # Services
    def add_service(self, s: Service) -> int:
        with self._conn() as c:
            cur = c.execute(
                """
                INSERT INTO services (company_id, code, name, category_id, unit_id, default_price, tax_rate, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (s.company_id, s.code, s.name, s.category_id, s.unit_id, s.default_price, s.tax_rate, s.created_at.isoformat(), s.updated_at.isoformat()),
            )
            return cur.lastrowid

    def get_service(self, service_id: int) -> Optional[Service]:
        with self._conn() as c:
            r = c.execute("SELECT * FROM services WHERE id = ?", (service_id,)).fetchone()
            if not r:
                return None
            return Service(id=r['id'], company_id=r['company_id'], code=r['code'], name=r['name'], category_id=r['category_id'], unit_id=r['unit_id'], default_price=r['default_price'], tax_rate=r['tax_rate'])

    def search_services(self, term: str) -> List[Service]:
        with self._conn() as c:
            rows = c.execute("SELECT * FROM services WHERE name LIKE ? OR code LIKE ? ORDER BY id", (f"%{term}%", f"%{term}%")).fetchall()
            return [Service(id=r['id'], company_id=r['company_id'], code=r['code'], name=r['name'], category_id=r['category_id'], unit_id=r['unit_id'], default_price=r['default_price'], tax_rate=r['tax_rate']) for r in rows]
