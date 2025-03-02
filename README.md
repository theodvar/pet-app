# Pet App

This is a web application for pet owners, built with Flask (backend), Angular (frontend), and PostgreSQL (database).

## Installation

### Backend
```bash
cd flask_backend
python -m venv venv
venv\Scripts\activate  # For Windows
# source venv/bin/activate  (For macOS/Linux)
pip install -r requirements.txt
python run.py


### Frontend

cd frontend
cd openlayers-demo
npm install
ng serve


### Database

Open DBeaver.
Click on "Database" then "New Connection".
Select PostgreSQL.
Enter your connection details:
Host: localhost
Port: 5432 (default PostgreSQL port)
Database: pets_db
Username: postgres
Password: postgres
Click Finish to connect.
Click on your PostgreSQL connection in DBeaver.
Right-click and choose "SQL Editor" then "New SQL Script".
Copy and paste the script from the file dump-pets_db-202503021728.sql into the SQL editor.
To execute everything, press CTRL + ENTER (or click the Execute button).
