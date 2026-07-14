"""
AGS ERP V2
Company Repository
"""

from app.core.base_repository import BaseRepository


class CompanyRepository(BaseRepository):

    table_name = "companies"

    def create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            commercial_name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            rc TEXT,
            nif TEXT,
            nis TEXT,
            ai TEXT,
            currency TEXT DEFAULT 'DZD',
            language TEXT DEFAULT 'fr',
            company_id INTEGER,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            website TEXT,
            bank TEXT,
            rib TEXT,
            iban TEXT,
            swift TEXT,
            vat TEXT,
            logo TEXT
        )
        """
        self.execute(query)

    def create(self, company):

        query = """
        INSERT INTO companies (
            code,
            name,
            commercial_name,
            phone,
            email,
            address,
            rc,
            nif,
            nis,
            ai,
            currency,
            language,
            company_id,
            is_active,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        params = (
            company.code,
            company.name,
            company.commercial_name,
            company.phone,
            company.email,
            company.address,
            company.rc,
            company.nif,
            company.nis,
            company.ai,
            company.currency,
            company.language,
            company.company_id,
            company.is_active,
            company.created_at,
            company.updated_at,
        )

        return self.execute(query, params)

    def get_by_id(self, record_id):

        query = """
        SELECT *
        FROM companies
        WHERE id = ?
        """

        return self.fetchone(query, (record_id,))


    def get_by_code(self, code):

        query = """
        SELECT *
        FROM companies
        WHERE code = ?
        """

        return self.fetchone(query, (code,))


    def list_all(self):

        query = """
        SELECT *
        FROM companies
        WHERE is_active = 1
        ORDER BY id DESC
        """

        return self.fetchall(query)


    def update(self, company):

        query = """
        UPDATE companies
        SET
            name = ?,
            commercial_name = ?,
            phone = ?,
            email = ?,
            address = ?,
            rc = ?,
            nif = ?,
            nis = ?,
            ai = ?,
            currency = ?,
            language = ?,
            updated_at = ?
        WHERE id = ?
        """

        params = (
            company.name,
            company.commercial_name,
            company.phone,
            company.email,
            company.address,
            company.rc,
            company.nif,
            company.nis,
            company.ai,
            company.currency,
            company.language,
            company.updated_at,
            company.id,
        )

        return self.execute(query, params)


    def deactivate(self, company_id):

        query = """
        UPDATE companies
        SET
            is_active = 0,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """

        return self.execute(query, (company_id,))
