from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from airflow import DAG
from airflow.operators.python import PythonOperator

# Airflow Docker ağında PostgreSQL'e bağlanmak için bağlantı dizesi
DB_URI = "postgresql+psycopg2://datauser:datapass@project-postgres:5432/enterprise_dwh"

def load_raw_data():
    engine = create_engine(DB_URI)
    
    # CSV dosyalarını okuyup PostgreSQL raw şemasına yazma
    customers_df = pd.read_csv('/opt/airflow/data/generated/customers.csv')
    customers_df.to_sql('customers', engine, schema='raw', if_exists='append', index=False)
    
    products_df = pd.read_csv('/opt/airflow/data/generated/products.csv')
    products_df.to_sql('products', engine, schema='raw', if_exists='append', index=False)
    
    orders_df = pd.read_csv('/opt/airflow/data/generated/orders.csv')
    orders_df.to_sql('orders', engine, schema='raw', if_exists='append', index=False)
    print("Ham veriler (raw) başarıyla yüklendi.")

def build_staging():
    print("Staging katmanı işlemleri (Gelecek sürümlerde eklenecek).")

def build_ods():
    engine = create_engine(DB_URI)
    query = """
    TRUNCATE TABLE ods.orders;
    INSERT INTO ods.orders (order_id, customer_id, order_date, status, amount, loaded_at)
    SELECT order_id, customer_id, order_date, status, amount, CURRENT_TIMESTAMP
    FROM raw.orders;
    """
    with engine.begin() as conn:
        conn.execute(text(query))
    print("ODS katmanı güncellendi.")

def build_dwh():
    engine = create_engine(DB_URI)
    query = """
    TRUNCATE TABLE dwh.sales_daily;
    INSERT INTO dwh.sales_daily (sales_date, order_count, customer_count, gross_amount)
    SELECT 
        order_date AS sales_date,
        COUNT(order_id) AS order_count,
        COUNT(DISTINCT customer_id) AS customer_count,
        SUM(amount) AS gross_amount
    FROM ods.orders
    GROUP BY order_date;
    """
    with engine.begin() as conn:
        conn.execute(text(query))
    print("DWH katmanı güncellendi.")

def collect_quality_metrics():
    print("Kalite metrikleri hesaplama adımı (Bir sonraki görevde kodlanacak).")

with DAG(
    dag_id="main_etl_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["thesis", "data-quality"],
) as dag:
    
    task_load_raw = PythonOperator(
        task_id="load_raw_data",
        python_callable=load_raw_data,
    )
    
    task_build_staging = PythonOperator(
        task_id="build_staging",
        python_callable=build_staging,
    )
    
    task_build_ods = PythonOperator(
        task_id="build_ods",
        python_callable=build_ods,
    )
    
    task_build_dwh = PythonOperator(
        task_id="build_dwh",
        python_callable=build_dwh,
    )
    
    task_collect_quality = PythonOperator(
        task_id="collect_quality_metrics",
        python_callable=collect_quality_metrics,
    )
    
    # Proje kılavuzundaki DAG sıralaması
    task_load_raw >> task_build_staging >> task_build_ods >> task_build_dwh >> task_collect_quality