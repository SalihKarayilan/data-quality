-- Şemaların Oluşturulması
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS stg;
CREATE SCHEMA IF NOT EXISTS ods;
CREATE SCHEMA IF NOT EXISTS dwh;
CREATE SCHEMA IF NOT EXISTS bi;
CREATE SCHEMA IF NOT EXISTS quality;

-- Raw (Ham Veri) Katmanı Tabloları
CREATE TABLE IF NOT EXISTS raw.customers (
    customer_id BIGINT,
    customer_name TEXT,
    email TEXT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw.products (
    product_id BIGINT,
    product_name TEXT,
    unit_price NUMERIC(18,2)
);

CREATE TABLE IF NOT EXISTS raw.orders (
    order_id BIGINT,
    customer_id BIGINT,
    order_date DATE,
    status TEXT,
    amount NUMERIC(18,2),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ODS (Operasyonel Veri Deposu) Katmanı Tabloları
CREATE TABLE IF NOT EXISTS ods.orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    order_date DATE NOT NULL,
    status TEXT,
    amount NUMERIC(18,2),
    loaded_at TIMESTAMP
);

-- DWH (Veri Ambarı) Katmanı Tabloları
CREATE TABLE IF NOT EXISTS dwh.sales_daily (
    sales_date DATE PRIMARY KEY,
    order_count BIGINT,
    customer_count BIGINT,
    gross_amount NUMERIC(18,2)
);

-- Kalite (Quality) Katmanı Tabloları
CREATE TABLE IF NOT EXISTS quality.data_quality_metrics (
    id BIGSERIAL PRIMARY KEY,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    layer_name TEXT NOT NULL,
    table_name TEXT NOT NULL,
    column_name TEXT,
    row_count BIGINT,
    null_ratio NUMERIC,
    duplicate_ratio NUMERIC,
    freshness_delay_minutes NUMERIC,
    schema_hash TEXT
);

CREATE TABLE IF NOT EXISTS quality.injected_incidents (
    incident_id TEXT PRIMARY KEY,
    incident_type TEXT NOT NULL,
    injected_at TIMESTAMP NOT NULL,
    affected_table TEXT NOT NULL,
    affected_column TEXT,
    expected_root_cause TEXT,
    description TEXT
);