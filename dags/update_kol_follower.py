from __future__ import print_function
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

from crawler.kol import update_kols
from crawler.follower_id import crawl_kols_followers_ids
from crawler.follower import crawl_kols_followers

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
    dag_id="update_kol_follower",
    default_args=default_args,
    catchup=False,
    schedule_interval="0 17 * * *",
    tags=["update", "kol"],
)


# Update kols locations, ages, genders and add kols statistics
update_kols = PythonOperator(
    task_id="update_kols", python_callable=update_kols, dag=dag,
)

# Add more followers ids
crawl_kols_followers_ids = PythonOperator(
    task_id="crawl_kols_followers_ids",
    python_callable=crawl_kols_followers_ids,
    dag=dag,
)

# Crawl new followers profiles
crawl_kols_followers = PythonOperator(
    task_id="crawl_kols_followers", python_callable=crawl_kols_followers, dag=dag,
)


update_kols >> crawl_kols_followers_ids >> crawl_kols_followers
