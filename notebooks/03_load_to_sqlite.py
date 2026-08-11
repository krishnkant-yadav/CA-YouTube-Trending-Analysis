"""
03_load_to_sqlite.py
Loads the cleaned CSV into a SQLite database so the project can
demonstrate SQL analysis (not just pandas).
"""

import pandas as pd
import sqlite3

df = pd.read_csv("../data/cleaned/CAvideos_clean.csv")

conn = sqlite3.connect("../data/cleaned/ca_trending.db")
df.to_sql("trending_videos", conn, if_exists="replace", index=False)
conn.close()

print(f"Loaded {len(df):,} rows into ca_trending.db (table: trending_videos)")
