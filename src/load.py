import psycopg2
from psycopg2.extras import execute_values
from config import DB_CONN

UPSERT_GAMES = """
INSERT INTO games (appid, name, developer, publisher, release_date, genres)
VALUES %s
ON CONFLICT (appid) DO UPDATE SET
    name = EXCLUDED.name,
    developer = EXCLUDED.developer,
    publisher = EXCLUDED.publisher,
    release_date = EXCLUDED.release_date,
    genres = EXCLUDED.genres;
"""

UPSERT_SNAPSHOTS = """
INSERT INTO price_snapshots (snapshot_key, appid, snapshot_date, is_free, initial_price, final_price, discount_percent)
VALUES %s
ON CONFLICT (snapshot_key) DO UPDATE SET
    final_price = EXCLUDED.final_price,
    discount_percent = EXCLUDED.discount_percent;
"""

def load_data(games, snapshots):
    with psycopg2.connect(**DB_CONN) as conn:
        with conn.cursor() as cur:
            execute_values(cur, UPSERT_GAMES, [tuple(g.values()) for g in games])
            execute_values(cur, UPSERT_SNAPSHOTS, [tuple(s.values()) for s in snapshots])
        conn.commit()