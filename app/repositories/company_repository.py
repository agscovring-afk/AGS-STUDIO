from typing import Optional
from datetime import datetime

from app.models.company import Company
from app.repositories.base_repository import BaseRepository


class CompanyRepository(BaseRepository):

    def __init__(self, db_path=None):
        super().__init__(db_path)

    def create_table(self):
        with self.connection() as c:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS companies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    legal_name TEXT NOT NULL,
                    commercial_name TEXT,
                    code TEXT UNIQUE,
                    currency TEXT,
                    language TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
    def add(self, company: Company) -> int:
        with self.connection() as c:
            cur = c.execute(
                """
                INSERT INTO companies (legal_name, commercial_name, code, currency, language, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    company.legal_name,
                    company.commercial_name,
                    company.code,
                    company.currency,
                    company.language,
                    1 if company.is_active else 0,
                    company.created_at.isoformat() if isinstance(company.created_at, datetime) else str(company.created_at),
                    company.updated_at.isoformat() if isinstance(company.updated_at, datetime) else str(company.updated_at),
                ),
            )
            return cur.lastrowid

    def get(self, company_id: int) -> Optional[Company]:
        with self.connection() as c:
            row = c.execute("SELECT * FROM companies WHERE id = ?", (company_id,)).fetchone()
            if not row:
                return None
            # Parse datetime strings back into datetime objects where possible
            created_at = row["created_at"]
            updated_at = row["updated_at"]
            try:
                created_at = datetime.fromisoformat(created_at)
            except Exception:
                pass
            try:
                updated_at = datetime.fromisoformat(updated_at)
            except Exception:
                pass
            return Company(
                id=row["id"],
                legal_name=row["legal_name"],
                commercial_name=row["commercial_name"],
                code=row["code"],
                currency=row["currency"],
                language=row["language"],
                is_active=bool(row["is_active"]),
                created_at=created_at,
                updated_at=updated_at,
            )

    def list_all(self, include_inactive: bool = False):
        with self.connection() as c:
            if include_inactive:
                rows = c.execute("SELECT * FROM companies ORDER BY id").fetchall()
            else:
                rows = c.execute("SELECT * FROM companies WHERE is_active = 1 ORDER BY id").fetchall()
            results = []
            for row in rows:
                created_at = row["created_at"]
                updated_at = row["updated_at"]
                try:
                    created_at = datetime.fromisoformat(created_at)
                except Exception:
                    pass
                try:
                    updated_at = datetime.fromisoformat(updated_at)
                except Exception:
                    pass
                results.append(
                    Company(
                        id=row["id"],
                        legal_name=row["legal_name"],
                        commercial_name=row["commercial_name"],
                        code=row["code"],
                        currency=row["currency"],
                        language=row["language"],
                        is_active=bool(row["is_active"]),
                        created_at=created_at,
                        updated_at=updated_at,
                    )
                )
            return results

    def update(self, company: Company) -> None:
        with self.connection() as c:
            c.execute(
                """
                UPDATE companies SET legal_name = ?, commercial_name = ?, code = ?, currency = ?, language = ?, is_active = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    company.legal_name,
                    company.commercial_name,
                    company.code,
                    company.currency,
                    company.language,
                    1 if company.is_active else 0,
                    company.updated_at.isoformat() if isinstance(company.updated_at, datetime) else str(company.updated_at),
                    company.id,
                ),
            )

    def deactivate(self, company_id: int) -> None:
        with self.connection() as c:
            c.execute("UPDATE companies SET is_active = 0, updated_at = ? WHERE id = ?", (datetime.utcnow().isoformat(), company_id))


