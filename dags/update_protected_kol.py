from __future__ import print_function
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

from crawler.protected_kol import crawl_protected_kols

default_args = {
    "owner": "Airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 1, 1),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    dag_id="update_protected_kol",
    default_args=default_args,
    catchup=False,
    schedule_interval="0 0 * * *",
    tags=["protected", "kol"],
)


crawl_protected_kols = PythonOperator(
    task_id="crawl_protected_kols", python_callable=crawl_protected_kols, dag=dag,
)


crawl_protected_kols
