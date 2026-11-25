from decimal import Decimal
from datetime import datetime

def parse_date(value: str | None):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%d %b, %Y").date()
    except ValueError:
        return None

def transform_game(raw: dict, appid: int, snapshot_date):
    game = {
        "appid": appid,
        "name": raw.get("name"),
        "developer": ", ".join(raw.get("developers", [])),
        "publisher": ", ".join(raw.get("publishers", [])),
        "release_date": parse_date(raw.get("release_date", {}).get("date")),
        "genres": ", ".join(g["description"] for g in raw.get("genres", [])),
    }
    price = raw.get("price_overview")
    if price is None:
        snapshot = {
            "snapshot_key": f"{appid}_{snapshot_date.isoformat()}",
            "appid": appid,
            "snapshot_date": snapshot_date,
            "is_free": True,
            "initial_price": None,
            "final_price": None,
            "discount_percent": 0,
        }
    else:
        snapshot = {
            "snapshot_key": f"{appid}_{snapshot_date.isoformat()}",
            "appid": appid,
            "snapshot_date": snapshot_date,
            "is_free": False,
            "initial_price": Decimal(price["initial"]) / 100,
            "final_price": Decimal(price["final"]) / 100,
            "discount_percent": price["discount_percent"],
        }
    return game, snapshot