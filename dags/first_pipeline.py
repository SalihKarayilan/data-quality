from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def say_hello():
    print("İlk veri pipeline'ı çalıştı")

with DAG(
    dag_id="first_data_quality_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["thesis", "data-quality"],
) as dag:
    test_task = PythonOperator(
        task_id="test_task",
        python_callable=say_hello,
    )