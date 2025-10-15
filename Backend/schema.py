import sqlite3




# Database path
db_path = "urban_mobility.db"




# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()




# Drop table if exists (for reruns)
cursor.execute("DROP TABLE IF EXISTS trips;")




# Create table with normalized schema
cursor.execute("""
CREATE TABLE trips (
    id TEXT PRIMARY KEY,
    vendor_id INTEGER,
    pickup_datetime TEXT,
    dropoff_datetime TEXT,
    passenger_count INTEGER,
    pickup_longitude REAL,
    pickup_latitude REAL,
    dropoff_longitude REAL,
    dropoff_latitude REAL,
    store_and_fwd_flag TEXT,
    trip_duration INTEGER,
    trip_duration_min REAL,
    trip_distance_km REAL,
    speed_kmh REAL
);
""")




# Create indexes
cursor.execute("CREATE INDEX idx_pickup_datetime ON trips(pickup_datetime);")
cursor.execute("CREATE INDEX idx_vendor_id ON trips(vendor_id);")
cursor.execute("CREATE INDEX idx_trip_duration_min ON trips(trip_duration_min);")




conn.commit()
conn.close()




print(" Database schema with indexes created successfully (urban_mobility.db)")




