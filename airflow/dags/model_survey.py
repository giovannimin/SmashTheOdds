# -*- coding: utf-8 -*-
"""
Created on 29/08/2023 17:19
@author: Lu6D
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
    dag_id='Check metrics',
    description='Verifies les métriques du nouveau modèle',
    tags=['SmashTheOdds'],
    default_args=default_args,
    schedule_interval=timedelta(minutes=1),
    catchup=False
)

with dag:
    check_metrics_task = BashOperator(
        task_id='check metrics',
        bash_command='python3 /opt/airflow/sources/model_testing.py',
        retries=1
    )


    check_metrics_task
