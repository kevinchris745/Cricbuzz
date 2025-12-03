# 🏏 Cricbuzz LiveStats – Streamlit Dashboard

Cricbuzz LiveStats is a Streamlit-based interactive dashboard that displays
real-time and historical cricket statistics.  
It pulls data from the Cricbuzz API, stores structured results in a MySQL
database, and visualizes batting, bowling, and match information.

---

## 📌 Features

### 🔹 1. Live Match Updates  
- Displays current live cricket matches  
- Scorecards, match summaries, team comparison stats  

### 🔹 2. Top Player Statistics  
- Most Runs (from SQL)  
- Highest Scores (from CSV → SQL)  
- Most Wickets (from CSV → SQL)  
- Clean visual tables powered by Pandas + Streamlit  
- Ability to filter, sort, and download CSV files  

### 🔹 3. SQL Query Explorer  
- Run custom SQL inside the app  
- View, filter, sort database tables  
- Direct connection to MySQL with PyMySQL  

### 🔹 4. Player CRUD Operations  
- Add player stats  
- Update/Delete player stats  
- Validate inputs  
- All operations stored in MySQL  

### 🔹 5. Modular Project Structure  
- Organized into `pages/`, `utils/`
- Easy to scale and maintain

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/cricbuzz_livestats.git
cd cricbuzz_livestats

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # macOS/Linux

# Install dependencies: 
pip install -r requirements.txt

#Configure Database:
CREATE DATABASE cricbuzz;

Update credentials inside:
utils/db_connection.py
pages/sql_queries.py
pages/top_player_stats.py
pages/crud_operations.py

Configuratkion Setup: 
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'cricbuzz'
}

To run App:
streamlit run app.py

*** Important notice***
please update path directory of the downloaded CSV files for code to run 

## 🗂 Project Structure

cricbuzz_livestats/
│── app.py # Main Streamlit app entry point
│── requirements.txt # Python package dependencies
│── README.md # Project documentation
│── Bowling.csv for loading data from csv file 
│── Highest team wins.csv for loading data from csv file 
│── highest_runs.csv for loading data from csv file 
│── matches.csv for loading data from csv file 
│── series.csv for loading data from csv file 
│── venues.csv for loading data from csv file 

├── pages/ # Streamlit multi-page files
│ ├── crud_operations.py # CRUD on SQL player tables
│ ├── Home.py # homepage
│ ├── live_matches.py # Live match API dashboard
│ ├── sql_queries.py # SQL query explorer
│ ├── top_player_stats.py # Batting & bowling stats dashboard
│
├── utils/
│ └── db_connection.py # MySQL connection helper

If you would like improvements or new features, feel free to reach out!
Author: Kevin Christopher

GitHub: Kevinchris745
