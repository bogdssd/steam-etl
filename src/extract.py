import requests
import json
import time
from datetime import date
from config import STEAM_API_URL, APP_IDS, RAW_DIR, RETRY_COUNT, RETRY_DELAY

def fetch_game_data(appid: int) -> dict | None:
    params = {"appids": appid, "cc": "ru"}
    for attempt in range(RETRY_COUNT):
        try:
            response = requests.get(STEAM_API_URL, params=params, timeout=10)
            if response.status_code == 429:
                time.sleep(RETRY_DELAY * (2 ** attempt))
                continue
            response.raise_for_status()
            data = response.json()
            if not data[str(appid)]["success"]:
                return None
            return data[str(appid)]["data"]
        except requests.RequestException:
            if attempt == RETRY_COUNT - 1:
                raise
            time.sleep(RETRY_DELAY * (2 ** attempt))
    return None

def save_raw(appid: int, data: dict) -> None:
    RAW_DIR.mkdir(exist_ok=True)
    path = RAW_DIR / f"{appid}_{date.today().isoformat()}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def run_extract():
    for appid in APP_IDS:
        data = fetch_game_data(appid)
        if data:
            save_raw(appid, data)
            print(f"Saved {appid}")