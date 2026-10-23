from datetime import datetime
from sqlalchemy import create_engine, text

# Host (Windows) üzerinden bağlandığımız için localhost ve 5433 portu
DB_URI = "postgresql+psycopg2://datauser:datapass@localhost:5433/enterprise_dwh"


def inject_anomalies():
    engine = create_engine(DB_URI)

    with engine.begin() as conn:
        now = datetime.now()

        # 1. Anomali: ODS tablosunda ani NULL artışı
        # Senaryo: Upstream bir API hatası yüzünden bazı siparişlerde müşteri ID'leri kayboldu. (%5 oranında)
        null_incident_id = f"INC-NULL-{now.strftime('%Y%m%d%H%M%S')}"
        conn.execute(text("""
                          UPDATE ods.orders
                          SET customer_id = NULL
                          WHERE order_id IN (SELECT order_id
                                             FROM ods.orders
                                             ORDER BY RANDOM()
                              LIMIT (SELECT COUNT (*) / 20 FROM ods.orders)
                              )
                          """))

        # Bu durumu referans (Ground Truth) tablomuza logluyoruz
        conn.execute(text("""
                          INSERT INTO quality.injected_incidents
                          (incident_id, incident_type, injected_at, affected_table, affected_column,
                           expected_root_cause, description)
                          VALUES (:id, 'NULL_SPIKE', :time, 'ods.orders', 'customer_id', 'UPSTREAM_API_FAILURE',
                                  'Kasıtlı olarak %5 oranında customer_id NULL yapıldı.')
                          """), {"id": null_incident_id, "time": now})

        # 2. Anomali: Raw tablosuna mükerrer kayıt (Duplicate) ekleme
        # Senaryo: ETL pipeline tekrar çalıştı (retry) ve eski verileri yanlışlıkla bir daha yazdı. (500 adet)
        dup_incident_id = f"INC-DUP-{now.strftime('%Y%m%d%H%M%S')}"
        conn.execute(text("""
                          INSERT INTO raw.orders (order_id, customer_id, order_date, status, amount, loaded_at)
                          SELECT order_id, customer_id, order_date, status, amount, loaded_at
                          FROM raw.orders
                          ORDER BY RANDOM() LIMIT 500;
                          """))

        # İkinci durumu logluyoruz
        conn.execute(text("""
                          INSERT INTO quality.injected_incidents
                          (incident_id, incident_type, injected_at, affected_table, affected_column,
                           expected_root_cause, description)
                          VALUES (:id, 'DUPLICATE_ROWS', :time, 'raw.orders', NULL, 'PIPELINE_RETRY_ERROR',
                                  'Kasıtlı olarak 500 adet mükerrer sipariş kaydı eklendi.')
                          """), {"id": dup_incident_id, "time": now})

    print("Hata enjeksiyonu başarıyla tamamlandı. Yapay anormallikler quality.injected_incidents tablosuna loglandı.")


if __name__ == "__main__":
    inject_anomalies()