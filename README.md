# Urban-Mobility-Data-App

Setup Instructions

Before running the project, make sure you have Python 3.12+ installed.

1. Clone the repository
   git clone https://github.com/AHIRWE1/Urban\_Mobility\_Data\_Explorer.git
   cd Urban\_Mobility\_Data\_Explorer
2. Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate     # Mac/Linux
   venv\\Scripts\\activate        # Windows
3. Install dependencies
   pip install -r requirements.txt
4. Run the scripts in order
   python data\_cleaning.py
   python schema.py
   python load\_data\_to\_db.py
   python init\_db.py
   python app.py

API Endpoints

Once Flask is running, test the API with:

Summary: http://127.0.0.1:5000/api/summary

Vendor Share: http://127.0.0.1:5000/api/vendor\_share

Trips Over Time: http://127.0.0.1:5000/api/trips\_over\_time

Average Speed by Passenger: http://127.0.0.1:5000/api/avg\_speed\_by\_passenger

Click on the http://127.0.0.1:5000/ while the server is running to tak you to the frontend dashboard



Architecture slide flow: data\_cleaning.py → schema.py → load\_data\_to\_db.py → app.py (Flask) → index.html (Chart.js).



✅ Notes

Ensure data/raw/train.csv exists before running the pipeline.

Each contributor should:

Download the train.csv file here https://surli.cc/payzlg

Create their own local versions of these files.

Ensure these train.csv file remain ignored in Git commits

Ensure that train.csv exists in the data/raw/ folder before running

The cleaned data is stored in data/cleaned/train\_cleaned.csv.

The database file urban\_mobility.db is auto-generated after running load\_data\_to\_db.py.



.gitignore Setup
To prevent pushing large files to GitHub, a .gitignore file was created including:
train.csv
train\_cleaned.csv
data/cleaned/train\_cleaned.csv
urban\_mobility.db





Video Walkthrough Link - https://youtu.be/Kspl7Q-KAQM





.

