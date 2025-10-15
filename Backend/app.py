from flask import Flask, jsonify, render_template
import sqlite3
import os
from flask_cors import CORS

# Serve frontend files (templates + static) from the Frontend directory
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Frontend')
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='', template_folder=FRONTEND_DIR)
CORS(app)

# ✅ Build the correct absolute path to the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'urban_mobility.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # Serve the frontend index.html
    return render_template('index.html')

# --- Summary API ---
@app.route('/api/summary')
def summary():
    conn = get_db_connection()
    query = '''
    SELECT
        COUNT(*) AS total_trips,
        ROUND(AVG(trip_duration_min), 2) AS avg_duration_min
    FROM trips;
    '''
    summary = conn.execute(query).fetchone()

    # Vendor average speed
    vendor_query = '''
    SELECT vendor_id, ROUND(AVG(speed_kmh), 2) AS avg_speed
    FROM trips
    WHERE speed_kmh > 0
    GROUP BY vendor_id;
    '''
    vendor_rows = conn.execute(vendor_query).fetchall()
    conn.close()

    vendor_speeds = {f"vendor_{row['vendor_id']}_avg_speed": row['avg_speed'] for row in vendor_rows}

    return jsonify({
        "total_trips": summary["total_trips"],
        "avg_duration_min": summary["avg_duration_min"],
        **vendor_speeds
    })

# --- Vendor Share ---
@app.route('/api/vendor_share')
def vendor_share():
    conn = get_db_connection()
    query = '''
    SELECT vendor_id, COUNT(*) AS trip_count
    FROM trips
    GROUP BY vendor_id;
    '''
    rows = conn.execute(query).fetchall()
    conn.close()
    return jsonify([{ "vendor_id": row["vendor_id"], "trip_count": row["trip_count"] } for row in rows])

# --- Trips Over Time ---
@app.route('/api/trips_over_time')
def trips_over_time():
    conn = get_db_connection()
    query = '''
    SELECT strftime('%Y-%m-%d', pickup_datetime) AS pickup_date,
           COUNT(*) AS trip_count
    FROM trips
    GROUP BY pickup_date
    ORDER BY pickup_date;
    '''
    rows = conn.execute(query).fetchall()
    conn.close()
    return jsonify([{ "pickup_date": row["pickup_date"], "trip_count": row["trip_count"] } for row in rows])

# --- Average Speed by Passenger ---
@app.route('/api/avg_speed_by_passenger')
def avg_speed_by_passenger():
    conn = get_db_connection()
    query = '''
    SELECT passenger_count, ROUND(AVG(speed_kmh), 2) AS avg_speed
    FROM trips
    WHERE passenger_count > 0
    GROUP BY passenger_count
    ORDER BY passenger_count;
    '''
    rows = conn.execute(query).fetchall()
    conn.close()
    return jsonify([{ "passenger_count": row["passenger_count"], "avg_speed": row["avg_speed"] } for row in rows])

if __name__ == '__main__':
    app.run(debug=True)
