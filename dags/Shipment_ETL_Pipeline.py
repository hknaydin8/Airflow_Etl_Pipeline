from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 5, 7),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


dag = DAG(
        'pl_Group0_Shipment_Data',
        default_args=default_args,
        description='Transfer data from MongoDB to PostgreSQL',
        schedule_interval='@daily',
        )
start_task = DummyOperator(task_id='start_task', dag=dag)

data_generate_task = BashOperator(
        task_id='Data_Generate_Task_MongoDB',
        bash_command='python /opt/airflow/python_scripts/Shipment_Data_Import.py',
        dag=dag,
        )

transfer_data_task = BashOperator(
        task_id='Data_Transfer_task_PostgreSQL',
        bash_command='python /opt/airflow/python_scripts/MongoDB_to_PostgreDB.py',
        dag=dag,
        trigger_rule='all_done' # upstreamtask hata alması durumunda da çalışması için eklendi.
        )
end_task = DummyOperator(task_id='end_task', dag=dag)


start_task >> data_generate_task >> transfer_data_task >> end_task