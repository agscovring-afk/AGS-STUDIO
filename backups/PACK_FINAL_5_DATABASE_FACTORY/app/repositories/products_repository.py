import sqlite3

DB_PATH = "ags_studio.db"


class ProductsRepository:
    def get_connection(self):
        return sqlite3.connect(DB_PATH)

    def get_all(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, reference, price, quantity FROM products")
        rows = cur.fetchall()
        conn.close()
        return rows

    def create(self, data):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO products (name, reference, price, quantity) VALUES (?, ?, ?, ?)",
            (
                data.get("name", ""),
                data.get("reference", ""),
                float(data.get("price") or 0),
                int(data.get("quantity") or 0),
            ),
        )
        conn.commit()
        conn.close()
        return data

    def update(self, data):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE products SET name=?, reference=?, price=?, quantity=? WHERE id=?",
            (
                data.get("name", ""),
                data.get("reference", ""),
                float(data.get("price") or 0),
                int(data.get("quantity") or 0),
                data.get("id"),
            ),
        )
        conn.commit()
        conn.close()
        return data

    def delete(self, record_id):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        return record_id
