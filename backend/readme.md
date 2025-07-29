Backend Setup for FastAPI + SQLite (Region-Site-Device + Login)
This backend project is built using FastAPI and SQLite. It supports login functionality and management of Region, Site, and Device entities.

⚙️ Prerequisites
Make sure you have Python 3.8+ installed. Then install the required packages.

bash
Copy
Edit
pip install -r requirements.txt


🛠️ Setup Steps

1. Initialize Databases
Run the following script to create the required SQLite databases:

bash
Copy
Edit
python setup_db.py
This will:

Create details.db with a default login user:

Username: admin

Password: admin123

Create and seed auth.db with:

Regions: North, South

Sites: NorthSiteA, SouthSiteB

Devices: 192.168.1.1, 192.168.1.2

2. (Optional) Seed Additional Data
If you want to re-run or add more region/site/device data, use:

bash
Copy
Edit
python seed_data.py
This script inserts additional sample records if they don’t already exist.

3. Run the Backend Server
Start the FastAPI server:

bash
Copy
Edit
uvicorn app:app --reload --port 9090
The API will now be running at:
http://localhost:9090/

