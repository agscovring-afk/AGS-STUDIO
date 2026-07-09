
CREATE TABLE IF NOT EXISTS supplier (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    code TEXT NOT NULL UNIQUE,

    name TEXT NOT NULL,

    description TEXT,

    active BOOLEAN DEFAULT 1,

    created_at TIMESTAMP,

    updated_at TIMESTAMP

);

CREATE INDEX idx_supplier_code
ON supplier(code);

CREATE INDEX idx_supplier_name
ON supplier(name);
