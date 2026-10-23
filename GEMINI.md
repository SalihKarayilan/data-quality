\# Proje Bağlamı: Yapay Zekâ Destekli Veri Kalitesi ve Kök Neden Analizi

Hacettepe Üniversitesi Veri ve Bilgi Mühendisliği Yüksek Lisans Dönem Projesi. 

Amaç: Veri hatalarını (kısmi yükleme, NULL artışı, mükerrer kayıt, gecikme) tespit edip makine öğrenmesi (Isolation Forest, Naive Bayes) ile kök neden analizi yapmak.



\## Teknoloji Yığını (Stack)

\- \*\*Altyapı:\*\* Docker, Docker Compose

\- \*\*Orkestrasyon:\*\* Apache Airflow 3.3.2

\- \*\*Veritabanı:\*\* PostgreSQL 15 (`project-postgres` servisi, port: 5433, db: `enterprise\_dwh`)

\- \*\*Dil \& Kütüphaneler:\*\* Python 3.11+, Pandas, Numpy, Scikit-learn, Faker



\## Mimari ve Katmanlar

\- \*\*Veri Modeli Şemaları:\*\* raw, stg, ods, dwh, bi, quality

\- \*\*Dizinler:\*\* 

&#x20; - `dags/` (Airflow pipeline kodları)

&#x20; - `sql/` (Veritabanı şema ve DDL scriptleri)

&#x20; - `src/` (Veri üretimi ve ML betikleri)

&#x20; - `data/generated/` (Sentetik CSV çıktıları - Docker içine `/opt/airflow/data` olarak bağlıdır)



\## Geliştirme Kuralları (Kesinlikle Uyulacak)

1\. \*\*Veri Gizliliği:\*\* Asla gerçek şirket verisi kullanma. Testler için sadece `src/generate\_data.py` ile sentetik veri üretilecek.

2\. \*\*SQL ve Tablo Bütünlüğü:\*\* Veritabanı performans iyileştirmesi veya hata ayıklama yaparken mevcut SQL sorgularının ana yapısını ve tablo tanımlarını (DDL) kesinlikle değiştirme.

3\. \*\*Airflow Uyarıları:\*\* Otomatik e-posta veya hata bildirimleri için ekstra custom (özel) alert scriptleri yazma; sadece Airflow'un kendi yerleşik (built-in) alert mekanizmasını kullan.

4\. \*\*Kod Dili:\*\* Python scriptlerinde PEP-8 standartlarına uy. 



\## Sık Kullanılan Komutlar

\- Sanal Ortam Aktif Etme: `.\\.venv\\Scripts\\Activate.ps1`

\- Veri Üretimi: `python .\\src\\generate\_data.py`

\- Sistemi Başlat / Durdur: `docker compose up -d` / `docker compose down`

