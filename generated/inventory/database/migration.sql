
CREATE TABLE IF NOT EXISTS inventory (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    code TEXT NOT NULL UNIQUE,

    name TEXT NOT NULL,

    description TEXT,

    active BOOLEAN DEFAULT 1,

    created_at TIMESTAMP,

    updated_at TIMESTAMP

);

CREATE INDEX idx_inventory_code
ON inventory(code);

CREATE INDEX idx_inventory_name
ON inventory(name);
