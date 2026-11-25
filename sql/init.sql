CREATE TABLE IF NOT EXISTS games (
    appid INTEGER PRIMARY KEY,
    name TEXT,
    developer TEXT,
    publisher TEXT,
    release_date DATE,
    genres TEXT
);

CREATE TABLE IF NOT EXISTS price_snapshots (
    snapshot_key TEXT PRIMARY KEY,
    appid INTEGER,
    snapshot_date DATE,
    is_free BOOLEAN,
    initial_price NUMERIC,
    final_price NUMERIC,
    discount_percent INTEGER
);

CREATE TABLE IF NOT EXISTS discount_analysis (
    id SERIAL PRIMARY KEY,
    snapshot_date DATE,
    genre TEXT,
    avg_discount NUMERIC,
    games_with_discount INTEGER,
    max_discount INTEGER
);