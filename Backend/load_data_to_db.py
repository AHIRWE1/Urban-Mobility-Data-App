import sqlite3
import pandas as pd




# Paths
db_path = "urban_mobility.db"
csv_path = "data/cleaned/train_cleaned.csv"




# Load cleaned CSV into a DataFrame
print(" Loading cleaned data from CSV...")
df = pd.read_csv(csv_path)
print(f"Loaded {len(df):,} rows")




# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()




# Insert data into the trips table
print(" Inserting data into the database...")
df.to_sql("trips", conn, if_exists="replace", index=False)




# Verify insertion
count = cursor.execute("SELECT COUNT(*) FROM trips").fetchone()[0]
print(f" Successfully inserted {count:,} records into the trips table")




conn.close()
