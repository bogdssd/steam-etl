from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, date
import sys
sys.path.append("/opt/airflow/src")

from extract import run_extract
from transform import transform_game
from load import load_data
from quality import validate_snapshots
from config import APP_IDS, RAW_DIR
import json

default_args = {
    "owner": "student",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
    "execution_timeout": timedelta(minutes=30),
}

def extract_task():
    run_extract()

def transform_task():
    games, snapshots = [], []
    today = date.today()
    for appid in APP_IDS:
        path = RAW_DIR / f"{appid}_{today.isoformat()}.json"
        if path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            game, snapshot = transform_game(raw, appid, today)
            games.append(game)
            snapshots.append(snapshot)
    return {"games": games, "snapshots": snapshots}

def quality_task(ti):
    data = ti.xcom_pull(task_ids="transform_data")
    valid, errors = validate_snapshots(data["snapshots"])
    if errors:
        print(f"Ошибки качества: {errors}")
    return {"games": data["games"], "snapshots": valid}

def load_task(ti):
    data = ti.xcom_pull(task_ids="quality_check")
    load_data(data["games"], data["snapshots"])

with DAG(
    dag_id="steam_price_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1,
) as dag:
    extract = PythonOperator(task_id="extract_data", python_callable=extract_task)
    transform = PythonOperator(task_id="transform_data", python_callable=transform_task)
    quality = PythonOperator(task_id="quality_check", python_callable=quality_task)
    load = PythonOperator(task_id="load_data", python_callable=load_task)

    extract >> transform >> quality >> load