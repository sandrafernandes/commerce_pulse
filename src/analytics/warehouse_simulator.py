import sqlite3
import pandas as pd

DB_PATH = "analytics.db"

def save(df, table):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(table, conn, if_exists="append", index=False)
    conn.close()
