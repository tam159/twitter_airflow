from __future__ import print_function
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

from crawler.kol import crawl_new_kols
from crawler.follower_id import crawl_new_kols_followers_ids
from crawler.follower import crawl_new_kols_followers

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
    dag_id="new_follower_profile",
    default_args=default_args,
    catchup=False,
    schedule_interval=None,
    tags=["new", "kol"],
)

# Crawl new kols profiles
crawl_new_kols = PythonOperator(
    task_id="crawl_new_kols", python_callable=crawl_new_kols, dag=dag,
)

# Crawl new kols followers ids
crawl_new_kols_followers_ids = PythonOperator(
    task_id="crawl_new_kols_followers_ids",
    python_callable=crawl_new_kols_followers_ids,
    dag=dag,
)

# Crawl new kols followers profiles
crawl_new_kols_followers = PythonOperator(
    task_id="crawl_new_kols_followers",
    python_callable=crawl_new_kols_followers,
    dag=dag,
)

crawl_new_kols >> crawl_new_kols_followers_ids >> crawl_new_kols_followers
