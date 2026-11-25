def validate_snapshots(snapshots):
    valid, errors = [], []
    seen_keys = set()
    for s in snapshots:
        if not s.get("appid") or not s.get("snapshot_date"):
            errors.append(f"Missing required field: {s}")
            continue
        if s["snapshot_key"] in seen_keys:
            errors.append(f"Duplicate snapshot_key: {s['snapshot_key']}")
            continue
        seen_keys.add(s["snapshot_key"])
        if s["final_price"] is not None and s["final_price"] < 0:
            errors.append(f"Negative price: {s}")
            continue
        valid.append(s)
    return valid, errors