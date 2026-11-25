import os
from pathlib import Path

# API Steam
STEAM_API_URL = "https://store.steampowered.com/api/appdetails"

# Список игр для отслеживания (appid)
# Пример: 730 — CS2, 570 — Dota 2, 1245620 — Elden Ring
APP_IDS = [730, 570, 1245620, 1091500, 292030]

# Папки
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw"
QUALITY_DIR = BASE_DIR / "quality"

# Настройки повторов
RETRY_COUNT = 3
RETRY_DELAY = 2  # секунды

# Подключение к PostgreSQL (внутри Docker)
DB_CONN = {
    "host": "postgres",
    "port": 5432,
    "dbname": "steam_dwh",
    "user": "steam",
    "password": "steam",
}