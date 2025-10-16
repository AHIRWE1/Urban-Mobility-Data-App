# Urban-Mobility-Data-App

Setup Instructions

Before running the project, make sure you have Python 3.12+ installed.

1. Clone the repository
git clone https://github.com/AHIRWE1/Urban_Mobility_Data_Explorer.git
cd Urban_Mobility_Data_Explorer

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

3. Install dependencies
pip install -r requirements.txt

4. Run the scripts in order
python data_cleaning.py
python schema.py
python load_data_to_db.py
python init_db.py
python app.py

 API Endpoints

Once Flask is running, test the API with:

Summary: http://127.0.0.1:5000/api/summary

Vendor Share: http://127.0.0.1:5000/api/vendor_share

Trips Over Time: http://127.0.0.1:5000/api/trips_over_time

Average Speed by Passenger: http://127.0.0.1:5000/api/avg_speed_by_passenger

Click on the http://127.0.0.1:5000/ while the server is running to tak you to the frontend dashboard

✅ Notes

Ensure data/raw/train.csv exists before running the pipeline.

Each contributor should:

Download the train.csv file here https://surli.cc/payzlg

Create their own local versions of these files.

Ensure these train.csv file remain ignored in Git commits

Ensure that train.csv exists in the data/raw/ folder before running

The cleaned data is stored in data/cleaned/train_cleaned.csv.

The database file urban_mobility.db is auto-generated after running load_data_to_db.py.


 .gitignore Setup
To prevent pushing large files to GitHub, a .gitignore file was created including:
train.csv
train_cleaned.csv
data/cleaned/train_cleaned.csv
urban_mobility.db




.
