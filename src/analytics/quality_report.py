import sqlite3
import pandas as pd

DB_PATH = "src/analytics/analytics.db"  # ajusta se teu DB estiver noutro local

conn = sqlite3.connect(DB_PATH)

# Relatório simples de quantidade de pedidos
df_orders = pd.read_sql("SELECT COUNT(*) as total_orders FROM fact_events", conn)

print("\n=== DATA QUALITY REPORT ===")
print(df_orders)
print("===========================\n")

conn.close()
