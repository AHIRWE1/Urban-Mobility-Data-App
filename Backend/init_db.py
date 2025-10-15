import sqlite3
import pandas as pd
import os


# Get the absolute path to the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'urban_mobility.db')
CSV_PATH = os.path.join(BASE_DIR, 'Data', 'raw', 'train.csv')


def init_database():
    # Create a new database connection
    conn = sqlite3.connect(DB_PATH)
   
    # Read CSV file in chunks
    chunk_size = 100000  # Adjust based on your system's memory
   
    # Create the trips table
    conn.execute('''
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_id INTEGER,
        pickup_datetime DATETIME,
        dropoff_datetime DATETIME,
        passenger_count INTEGER,
        trip_duration_min FLOAT,
        speed_kmh FLOAT
    )
    ''')
   
    # Read and process the CSV file in chunks
    for chunk in pd.read_csv(CSV_PATH, chunksize=chunk_size):
        # Convert datetime columns
        chunk['pickup_datetime'] = pd.to_datetime(chunk['pickup_datetime'])
        chunk['dropoff_datetime'] = pd.to_datetime(chunk['dropoff_datetime'])
       
        # Calculate trip duration in minutes
        chunk['trip_duration_min'] = (chunk['dropoff_datetime'] - chunk['pickup_datetime']).dt.total_seconds() / 60
       
        # Calculate speed (assume trip_distance is in kilometers)
        # If trip_distance is in miles, multiply by 1.60934 to convert to km
        if 'trip_distance' in chunk.columns and 'trip_duration_min' in chunk.columns:
            chunk['speed_kmh'] = chunk.apply(
                lambda row: (row['trip_distance'] * 60) / row['trip_duration_min']
                if row['trip_duration_min'] > 0 else 0,
                axis=1
            )
        else:
            chunk['speed_kmh'] = 0
       
        # Select and rename columns as needed
        chunk = chunk[['vendor_id', 'pickup_datetime', 'dropoff_datetime',
                      'passenger_count', 'trip_duration_min', 'speed_kmh']]
       
        # Insert the data into the database
        chunk.to_sql('trips', conn, if_exists='append', index=False)
   
    # Create indices for better query performance
    conn.execute('CREATE INDEX IF NOT EXISTS idx_pickup_datetime ON trips(pickup_datetime)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_vendor_id ON trips(vendor_id)')
   
    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == '__main__':
    print("Initializing database...")
    init_database()
    print("Database initialization complete!")
