from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


def task_might_fail():

    raise Exception("Task failed.")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 5, 7),
}

dag = DAG(
    'example_dag',
    default_args=default_args,
    description='A simple DAG with tasks that might fail',
    schedule_interval=None,
)

# Tasklar
start_task = DummyOperator(task_id='start_task', dag=dag)
task1 = PythonOperator(
    task_id='task1',
    python_callable=task_might_fail,
    dag=dag,
)
task2 = DummyOperator(
    task_id='task2',
    dag=dag,
    trigger_rule='all_done'  # Burada hata olursa da task2 çalışacak
)
end_task = DummyOperator(task_id='end_task', dag=dag)

# Taskları bağlama
start_task >> task1 >> task2 >> end_task
