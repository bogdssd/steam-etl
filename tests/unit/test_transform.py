import pytest
from datetime import date
from decimal import Decimal
from src.transform import transform_game, parse_date

def test_transform_paid_game():
    raw = {
        "name": "Test Game",
        "developers": ["Dev Studio"],
        "publishers": ["Publisher Inc"],
        "release_date": {"date": "15 Jan, 2024"},
        "genres": [{"description": "Action"}],
        "price_overview": {
            "initial": 199900,
            "final": 99950,
            "discount_percent": 50,
        },
    }
    game, snapshot = transform_game(raw, appid=123, snapshot_date=date(2026, 1, 1))
    assert game["name"] == "Test Game"
    assert game["genres"] == "Action"
    assert snapshot["final_price"] == Decimal("999.50")
    assert snapshot["discount_percent"] == 50
    assert snapshot["is_free"] is False

def test_transform_free_game():
    raw = {"name": "Free Game", "release_date": {"date": "1 Jan, 2024"}}
    _, snapshot = transform_game(raw, appid=456, snapshot_date=date(2026, 1, 1))
    assert snapshot["is_free"] is True
    assert snapshot["final_price"] is None

def test_parse_date_invalid():
    assert parse_date("Coming soon") is None