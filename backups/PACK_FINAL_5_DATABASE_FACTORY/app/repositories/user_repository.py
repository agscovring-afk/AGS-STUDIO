"""Repository for users, roles and permissions."""
import sqlite3
from typing import Optional
from datetime import datetime
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission


class UserRepository:
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
                CREATE TABLE IF NOT EXISTS roles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    description TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS permissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    description TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS role_permissions (
                    role_id INTEGER,
                    permission_id INTEGER,
                    PRIMARY KEY (role_id, permission_id),
                    FOREIGN KEY(role_id) REFERENCES roles(id) ON DELETE CASCADE,
                    FOREIGN KEY(permission_id) REFERENCES permissions(id) ON DELETE CASCADE
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    username TEXT UNIQUE,
                    email TEXT,
                    password_hash TEXT,
                    role_id INTEGER,
                    is_active INTEGER DEFAULT 1,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY(role_id) REFERENCES roles(id)
                )
                """
            )

    def add_role(self, role: Role) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO roles (name, description, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (role.name, role.description, role.created_at.isoformat(), role.updated_at.isoformat()),
            )
            return cur.lastrowid

    def add_permission(self, perm: Permission) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO permissions (name, description, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (perm.name, perm.description, perm.created_at.isoformat(), perm.updated_at.isoformat()),
            )
            return cur.lastrowid

    def assign_permission(self, role_id: int, permission_id: int):
        with self._conn() as c:
            c.execute("INSERT OR IGNORE INTO role_permissions (role_id, permission_id) VALUES (?, ?)", (role_id, permission_id))

    def add_user(self, user: User) -> int:
        with self._conn() as c:
            cur = c.execute(
                """
                INSERT INTO users (company_id, username, email, password_hash, role_id, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user.company_id,
                    user.username,
                    user.email,
                    user.password_hash,
                    user.role_id,
                    1 if user.is_active else 0,
                    user.created_at.isoformat(),
                    user.updated_at.isoformat(),
                ),
            )
            return cur.lastrowid

    def get_user_by_username(self, username: str) -> Optional[User]:
        with self._conn() as c:
            row = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if not row:
                return None
            try:
                created_at = datetime.fromisoformat(row["created_at"])
            except Exception:
                created_at = row["created_at"]
            try:
                updated_at = datetime.fromisoformat(row["updated_at"])
            except Exception:
                updated_at = row["updated_at"]
            return User(
                id=row["id"],
                company_id=row["company_id"],
                username=row["username"],
                email=row["email"],
                password_hash=row["password_hash"],
                role_id=row["role_id"],
                is_active=bool(row["is_active"]),
                created_at=created_at,
                updated_at=updated_at,
            )
