from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


with DAG("my_dag", 
         start_date=datetime(2023, 7, 23), 
         schedule_interval = "@hourly", 
         catchup = False
         ) as dag:
            scrapping_upcoming = BashOperator(
                    task_id = "scrapping_upcoming",
                    bash_command = 'cd /opt/airflow/incoming_movies_spider && scrapy crawl incomingmovies',
            )

            scrapping_last_week = BashOperator(
                    task_id = "scrapping_last_week",
                    bash_command = "cd /opt/airflow/last_week_scrapping && scrapy crawl boxspider",
            )