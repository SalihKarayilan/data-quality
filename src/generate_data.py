from pathlib import Path
import numpy as np
import pandas as pd

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)

OUTPUT_DIR = Path("data/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Müşteriler
customers = pd.DataFrame({
    "customer_id": np.arange(1, 1001),
    "customer_name": [f"Customer {i}" for i in range(1, 1001)],
    "email": [f"customer{i}@example.com" for i in range(1, 1001)],
    "created_at": pd.Timestamp("2026-01-01")
})

# Ürünler
products = pd.DataFrame({
    "product_id": np.arange(1, 101),
    "product_name": [f"Product {i}" for i in range(1, 101)],
    "unit_price": rng.uniform(10, 500, 100).round(2)
})

# Siparişler (90 günlük veri üretimi - Yaklaşık 90,000 sipariş hedefi)
date_range = pd.date_range(start="2026-01-01", periods=90)
order_records = []
order_id_counter = 1

for current_date in date_range:
    is_weekend = current_date.weekday() >= 5
    # Hafta içi ~1000, Hafta sonu ~500 sipariş
    daily_order_count = int(rng.normal(loc=500, scale=50)) if is_weekend else int(rng.normal(loc=1000, scale=100))
    
    for _ in range(daily_order_count):
        order_records.append({
            "order_id": order_id_counter,
            "customer_id": rng.integers(1, 1001),
            "order_date": current_date,
            "status": rng.choice(["COMPLETED", "CANCELLED", "PENDING"], p=[0.80, 0.10, 0.10]),
            "amount": round(rng.uniform(20, 2000), 2)
        })
        order_id_counter += 1

orders = pd.DataFrame(order_records)

# Bazı gerçekçi NULL değerler ekleme (müşteri ID'si eksik gelen siparişler)
orders.loc[orders.sample(frac=0.01, random_state=42).index, "customer_id"] = None

customers.to_csv(OUTPUT_DIR / "customers.csv", index=False)
products.to_csv(OUTPUT_DIR / "products.csv", index=False)
orders.to_csv(OUTPUT_DIR / "orders.csv", index=False)

print(f"Generated {len(customers)} customers")
print(f"Generated {len(products)} products")
print(f"Generated {len(orders)} orders")