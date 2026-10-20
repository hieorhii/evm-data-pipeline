from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

from scripts.extract import extract_to_mongo
from scripts.load import load_to_clickhouse

default_args = {
    'owner': 'data_engineer',
    'start_date': datetime(2023, 1, 1),
}

with DAG('evm_daily_etl', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    task_extract = PythonOperator(
        task_id='extract_api_to_mongo',
        python_callable=extract_to_mongo
    )

    task_load = PythonOperator(
        task_id='load_mongo_to_clickhouse',
        python_callable=load_to_clickhouse
    )

    task_dbt = BashOperator(
        task_id='run_dbt_transformations',
        bash_command='cd /opt/airflow/dbt_web3 && dbt run --profiles-dir .'
    )

    task_extract >> task_load >> task_dbt