import os
from airflow import DAG
from airflow.operators.bash import BashOperator 
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 0,
}

# Get the directory of the current script (dag_sensor.py)
dag_folder = os.path.dirname(os.path.abspath(__file__))

dag = DAG(
    'sensor_data_pipeline',
    default_args=default_args,
    description='A DAG to process sensor data',
    schedule_interval=None,
)

task2 = BashOperator(
    task_id='run_step2_sensor',
    bash_command=f'python {dag_folder}/step2_cleansed_sensor.py',  
    dag=dag,
)

task2
