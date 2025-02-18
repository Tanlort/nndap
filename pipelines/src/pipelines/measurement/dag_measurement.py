import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 0,
}

# Get the directory of the current script (this will be where your scripts are stored)
dag_folder = os.path.dirname(os.path.abspath(__file__))

# Define the DAG
dag = DAG(
    'measurement_data_pipeline',
    default_args=default_args,
    description='A DAG to process raw measurement data and aggregate measurements',
    schedule_interval=None,  # Set the schedule interval here (e.g., cron expression, or None for manual run)
)

# Task to run step2_cleansed_measurement.py (data cleansing)
task1 = BashOperator(
    task_id='run_step2_cleansed_measurement',
    bash_command=f'python {dag_folder}/step2_cleansed_measurement.py',  
    dag=dag,
)

# Task to run weekly aggregation
task2_weekly = BashOperator(
    task_id='run_weekly_aggregation',
    bash_command=f'python {dag_folder}/step3_agreggate_measurement.py --aggregation_type weekly',  
    dag=dag,
)

# Task to run daily aggregation
task2_daily = BashOperator(
    task_id='run_daily_aggregation',
    bash_command=f'python {dag_folder}/step3_agreggate_measurement.py --aggregation_type daily',  
    dag=dag,
)

# Task to run monthly aggregation
task2_monthly = BashOperator(
    task_id='run_monthly_aggregation',
    bash_command=f'python {dag_folder}/step3_agreggate_measurement.py --aggregation_type monthly',  
    dag=dag,
)

# Task to run yearly aggregation
task2_yearly = BashOperator(
    task_id='run_yearly_aggregation',
    bash_command=f'python {dag_folder}/step3_agreggate_measurement.py --aggregation_type yearly',  
    dag=dag,
)

# Set the task execution order: step2 -> aggregations
task1 >> [task2_weekly, task2_daily, task2_monthly, task2_yearly]
