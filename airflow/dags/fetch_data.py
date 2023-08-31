# -*- coding: utf-8 -*-
"""
Created on 25/08/2023 16:15
@author: GiovanniMINGHELLI
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='Fetch data',
    description='Recuperer les données de matchsw',
    tags=['SmashTheOdds'],
    default_args=default_args,
    schedule_interval=timedelta(minutes=1),
    catchup=False
)

with dag:
    fetch_data_task = BashOperator(
        task_id='fetch_week_data',
        bash_command='python3 /opt/airflow/sources/update_table.py',
        retries=1
    )

    fetch_planning_task = BashOperator(
        task_id='fetch_planning',
        bash_command='python3 /opt/airflow/sources/update_planning.py',
        retries=1
    )

    [fetch_data_task, fetch_planning_task]
