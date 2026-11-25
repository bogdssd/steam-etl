from datetime import date
from decimal import Decimal
from src.quality import validate_snapshots

def test_validate_valid_snapshot():
    snapshots = [{
        "snapshot_key": "1_2026-01-01",
        "appid": 1,
        "snapshot_date": date(2026, 1, 1),
        "final_price": Decimal("100.00"),
    }]
    valid, errors = validate_snapshots(snapshots)
    assert len(valid) == 1
    assert errors == []

def test_validate_duplicate_keys():
    snapshots = [
        {"snapshot_key": "1_2026-01-01", "appid": 1, "snapshot_date": date(2026, 1, 1), "final_price": Decimal("100")},
        {"snapshot_key": "1_2026-01-01", "appid": 1, "snapshot_date": date(2026, 1, 1), "final_price": Decimal("200")},
    ]
    valid, errors = validate_snapshots(snapshots)
    assert len(valid) == 1
    assert len(errors) == 1
    assert "Duplicate" in errors[0]

def test_validate_negative_price():
    snapshots = [{
        "snapshot_key": "1_2026-01-01",
        "appid": 1,
        "snapshot_date": date(2026, 1, 1),
        "final_price": Decimal("-10.00"),
    }]
    valid, errors = validate_snapshots(snapshots)
    assert len(valid) == 0
    assert len(errors) == 1
    assert "Negative" in errors[0]

def test_validate_missing_fields():
    snapshots = [{"snapshot_key": "1_2026-01-01"}]
    valid, errors = validate_snapshots(snapshots)
    assert len(valid) == 0
    assert len(errors) == 1
    assert "Missing" in errors[0]