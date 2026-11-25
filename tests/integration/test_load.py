import pytest
import psycopg2
from datetime import date
from decimal import Decimal
from src.load import load_data

@pytest.fixture
def db_conn():
    conn = psycopg2.connect(
        host="postgres", port=5432, dbname="steam_dwh",
        user="steam", password="steam"
    )
    yield conn
    conn.close()

def test_load_is_idempotent(db_conn):
    games = [{
        "appid": 99999, "name": "Test Game", "developer": "D",
        "publisher": "P", "release_date": None, "genres": "Action"
    }]
    snapshots = [{
        "snapshot_key": "99999_2026-01-01",
        "appid": 99999,
        "snapshot_date": date(2026, 1, 1),
        "is_free": False,
        "initial_price": Decimal("100.00"),
        "final_price": Decimal("50.00"),
        "discount_percent": 50,
    }]

    # Загружаем дважды — дубликатов быть не должно
    load_data(games, snapshots)
    load_data(games, snapshots)

    with db_conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM price_snapshots WHERE appid = 99999")
        count = cur.fetchone()[0]
        assert count == 1

        # Чистим за собой
        cur.execute("DELETE FROM price_snapshots WHERE appid = 99999")
        cur.execute("DELETE FROM games WHERE appid = 99999")
    db_conn.commit()