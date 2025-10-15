# data_cleaning.py
import pandas as pd
import numpy as np
import os




# --- File paths (relative for portability) ---
raw_file = "data/raw/train.csv"
cleaned_file = "data/cleaned/train_cleaned.csv"
log_dir = "data/cleaned/"




# Ensure log directory exists
os.makedirs(log_dir, exist_ok=True)




# --- Step 1: Load dataset ---
print(" Loading raw dataset...")
df = pd.read_csv(raw_file)
print(f"Loaded {len(df):,} rows")




# --- Step 2: Convert datetime columns ---
print(" Converting datetime columns...")
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])




# --- Step 3: Derived Feature 1 — Trip duration in minutes ---
df['trip_duration_min'] = df['trip_duration'] / 60




# --- Step 4: Handle unrealistic trip durations ---
invalid_durations = df[(df['trip_duration_min'] < 1) | (df['trip_duration_min'] > 180)]
invalid_durations.to_csv(os.path.join(log_dir, "log_invalid_durations.csv"), index=False)
print(f"Logged {len(invalid_durations)} invalid duration records")




df = df[(df['trip_duration_min'] >= 1) & (df['trip_duration_min'] <= 180)]
print(f"Trips after duration filtering: {len(df):,}")




# --- Step 5: Handle unrealistic passenger counts ---
invalid_passengers = df[(df['passenger_count'] <= 0) | (df['passenger_count'] > 6)]
invalid_passengers.to_csv(os.path.join(log_dir, "log_invalid_passengers.csv"), index=False)
print(f"Logged {len(invalid_passengers)} invalid passenger records")




df = df[(df['passenger_count'] > 0) & (df['passenger_count'] <= 6)]
print(f"Trips after passenger filtering: {len(df):,}")




# --- Step 6: Handle out-of-bound coordinates ---
invalid_coords = df[~(
    (df['pickup_longitude'].between(-74.05, -73.70)) &
    (df['pickup_latitude'].between(40.55, 40.90)) &
    (df['dropoff_longitude'].between(-74.05, -73.70)) &
    (df['dropoff_latitude'].between(40.55, 40.90))
)]
invalid_coords.to_csv(os.path.join(log_dir, "log_invalid_coordinates.csv"), index=False)
print(f"Logged {len(invalid_coords)} invalid coordinate records")




df = df[
    (df['pickup_longitude'].between(-74.05, -73.70)) &
    (df['pickup_latitude'].between(40.55, 40.90)) &
    (df['dropoff_longitude'].between(-74.05, -73.70)) &
    (df['dropoff_latitude'].between(40.55, 40.90))
]
print(f"Trips after coordinate filtering: {len(df):,}")




# --- Step 7: Derived Feature 2 — Trip distance using Haversine formula ---
def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # Earth radius in km
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c




df['trip_distance_km'] = haversine(
    df['pickup_longitude'], df['pickup_latitude'],
    df['dropoff_longitude'], df['dropoff_latitude']
)




# --- Step 8: Derived Feature 3 — Speed (km/h) ---
df['speed_kmh'] = df['trip_distance_km'] / (df['trip_duration_min'] / 60)




# --- Step 9: Save cleaned dataset ---
df.to_csv(cleaned_file, index=False)
print(f" Cleaned dataset saved to {cleaned_file}")




# --- Optional Summary ---
print("\n Trip distance stats:")
print(df['trip_distance_km'].describe())




print("\n Speed stats:")
print(df['speed_kmh'].describe())
