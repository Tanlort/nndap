import os
from airflow import DAG
from airflow.operators.bash import BashOperator 
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 0,
}

# Get the directory of the current script (dag_cow.py)
dag_folder = os.path.dirname(os.path.abspath(__file__))

dag = DAG(
    'cow_data_pipeline',
    default_args=default_args,
    description='A DAG to process cow data',
    schedule_interval=None,
)

task2 = BashOperator(
    task_id='run_step2_cow',
    bash_command=f'python {dag_folder}/step2_cleansed_cow.py',  
    dag=dag,
)

task2
