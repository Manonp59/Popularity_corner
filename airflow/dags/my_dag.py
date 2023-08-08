from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 23),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    'my_dag',
    default_args=default_args,
    schedule_interval='0 8 * * 1',
    catchup=False,
) as dag:
            scrapping_upcoming = BashOperator(
                    task_id = "scrapping_upcoming",
                    bash_command = 'cd /opt/airflow/incoming_movies_spider && scrapy crawl incomingmovies',
            )

            scrapping_last_week = BashOperator(
                    task_id = "scrapping_last_week",
                    bash_command = "cd /opt/airflow/last_week_spider && scrapy crawl boxspider",
            )