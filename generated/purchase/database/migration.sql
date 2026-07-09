
CREATE TABLE IF NOT EXISTS purchase (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    code TEXT NOT NULL UNIQUE,

    name TEXT NOT NULL,

    description TEXT,

    active BOOLEAN DEFAULT 1,

    created_at TIMESTAMP,

    updated_at TIMESTAMP

);

CREATE INDEX idx_purchase_code
ON purchase(code);

CREATE INDEX idx_purchase_name
ON purchase(name);
