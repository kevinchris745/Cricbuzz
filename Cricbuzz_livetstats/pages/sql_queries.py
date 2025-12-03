import streamlit as st
import requests
import pymysql
import pandas as pd


# -------------------------------------------------------------------------------
# Question 1
# -------------------------------------------------------------------------------
#
# #team get players API
url = "https://cricbuzz-cricket.p.rapidapi.com/teams/v1/2/players"

headers = {
	"x-rapidapi-key": "0ba2806099msh254595567cb6039p166feajsn368b5ddfc66c",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
data = response.json()
players = data.get('player', [])
# print(data)

# print(f"Total entries in 'player': {len(players)}")

# --- Database Setup ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'database': 'cricbuzz',
    'password': 'Anvikkevin@123'
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
# print("Connected to DB")

# Create the players table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        player_id INT PRIMARY KEY,
        name VARCHAR(100),
        role VARCHAR(50),
        batting_style VARCHAR(100),
        bowling_style VARCHAR(100)
    )
""")
# print("Table checked/created")

# Insert players into the database
for player in players:
    if 'id' not in player:
        continue  # Skip headers like "BATSMEN", "BOWLER"

    player_id = int(player.get('id'))
    name = player.get('name')
    role = 'Unknown'  # As role info isn't directly given; you can enhance later
    batting_style = player.get('battingStyle', 'Unknown')
    bowling_style = player.get('bowlingStyle', 'Unknown')

    cursor.execute("""
        INSERT INTO players (player_id, name, role, batting_style, bowling_style)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            role = VALUES(role),
            batting_style = VALUES(batting_style),
            bowling_style = VALUES(bowling_style)
    """, (player_id, name, role, batting_style, bowling_style))

conn.commit()
# print("Data committed")

# --- Query to find all players ---
# Find all players who represent India. Display their full name, playing role, batting style, and bowling style.
cursor.execute("""
    SELECT name AS full_name, role AS playing_role, batting_style, bowling_style
    FROM players
""")
result = cursor.fetchall()
# print(result)

# Display using pandas for readability
q1 = pd.DataFrame(result, columns=['Full Name', 'Playing Role', 'Batting Style', 'Bowling Style'])
# print(q1)

cursor.close()
conn.close()
# --------------------------------------------------------------------------------------------------
#
#---------------------------------------------------------------------------------------------------
# Question 2:
# --------------------------------------------------------------------------------------------------
# API end point teams/get-schedules

from datetime import datetime
from pandas import value_counts

pd.set_option('display.max_columns', 6)
pd.set_option('display.width', 1000)

# --- Fetch API Data ---
url = "https://cricbuzz-cricket.p.rapidapi.com/teams/v1/2/schedule"

headers = {
    "x-rapidapi-key": "0ba2806099msh254595567cb6039p166feajsn368b5ddfc66c",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
data_SQL2 = response.json()
# print(data_SQL2.keys())  # Should include 'teamMatchesData'

# --- Database Setup ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'database': 'cricbuzz',
    'password': 'Anvikkevin@123'
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
# print("Connected to DB")

# Create table with unique constraint
cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        match_id INT PRIMARY KEY AUTO_INCREMENT,
        description VARCHAR(255),
        team1_name VARCHAR(100),
        team2_name VARCHAR(100),
        venue_name VARCHAR(100),
        city VARCHAR(100),
        match_date DATETIME,
        UNIQUE KEY unique_match (description, team1_name, team2_name, venue_name, city, match_date)
    )
""")
conn.commit()

# Insert Match Data using INSERT IGNORE
for item in data_SQL2.get('teamMatchesData', []):
    match_details = item.get('matchDetailsMap', {})
    matches = match_details.get('match', [])

    for match in matches:
        match_info = match['matchInfo']

        description = match_info.get('matchDesc', 'Unknown').strip()
        team1 = match_info.get('team1', {}).get('teamName', 'Unknown').strip()
        team2 = match_info.get('team2', {}).get('teamName', 'Unknown').strip()
        venue_name = match_info.get('venueInfo', {}).get('ground', 'Unknown').strip()
        city = match_info.get('venueInfo', {}).get('city', 'Unknown').strip()

        start_date_ms = match_info.get('startDate')
        match_date = datetime.utcfromtimestamp(int(start_date_ms) / 1000) if start_date_ms else datetime(1970, 1, 1)

        # print("Inserting:", description, team1, team2, venue_name, city, match_date)

        cursor.execute("""
            INSERT IGNORE INTO matches (description, team1_name, team2_name, venue_name, city, match_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (description, team1, team2, venue_name, city, match_date))

conn.commit()

# --- Query Data ---
cursor.execute("""
    SELECT description, team1_name, team2_name, venue_name, city, match_date
    FROM matches
    ORDER BY match_date DESC
""")

results = cursor.fetchall()
q2 = pd.DataFrame(results, columns=['Match Description', 'Team 1', 'Team 2', 'Venue', 'City', 'Date'])
# print("Before removing duplicates:", len(q2))
# q2 = q2.drop_duplicates(subset=['Match Description', 'Team 1', 'Team 2', 'Venue', 'City', 'Date'])
# print("After removing duplicates:", len(q2))
# q2 = q2.reset_index(drop=True)
# print(q2)

# ---------------------------------------------------------------------------------------------
# Question 3
# ---------------------------------------------------------------------------------------------

# API end point stats/get-records

import requests
import pandas as pd
import pymysql
import re

# ********** API CONFIG **********
import requests

url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"

querystring = {"statsType":"mostRuns"}

headers = {
	"x-rapidapi-key": "667adf478dmsh3388b2ca3f77dd6p1c646cjsne88d8510fdff",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# ********** CHECK HEADERS EXIST **********
if "headers" not in data or "values" not in data:
    raise ValueError("API did NOT return expected headers/values. Full JSON:", data)

headers_list = data["headers"]     # ['Batter','M','I','R','Avg']
rows_list = data["values"]         # list of players

# ********** CLEANING LOGIC **********
def is_numeric(val):
    return bool(re.match(r"^-?\d+(\.\d+)?$", str(val)))

cleaned_rows = []

for row in rows_list:
    vals = row["values"]

    # Remove rank/index
    if is_numeric(vals[0]) and re.search(r"[A-Za-z]", vals[1]):
        vals = vals[1:]   # Drop first element

    # Ensure correct length
    if len(vals) > len(headers_list):
        vals = vals[:len(headers_list)]
    if len(vals) < len(headers_list):
        vals += [""] * (len(headers_list) - len(vals))

    cleaned_rows.append(vals)

# ********** BUILD DATAFRAME **********
df = pd.DataFrame(cleaned_rows, columns=headers_list)

# Convert columns
convert_cols = ["M", "I", "R", "Avg"]
for col in convert_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ********** PICK TOP 10 **********
top10 = df.sort_values(by="R", ascending=False).head(10)

# ********** MYSQL SAVE **********
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'database': 'cricbuzz',
    'password': 'Anvikkevin@123'
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

# Ensure table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS top_odi_scorers (
    player_name VARCHAR(50),
    matches INT,
    innings INT,
    runs INT,
    avg FLOAT
)
""")

cursor.execute("TRUNCATE TABLE top_odi_scorers")

# Insert each row
for _, r in top10.iterrows():
    cursor.execute("""
        INSERT INTO top_odi_scorers (player_name, matches, innings, runs, avg)
        VALUES (%s, %s, %s, %s, %s)
    """, (r["Batter"], int(r["M"]), int(r["I"]), int(r["R"]), float(r["Avg"])))

conn.commit()
cursor.close()
conn.close()

# print("Most Runs ODI Table Updated Successfully")


# -------------------------------------------------------------------------
# Question 4
# -------------------------------------------------------------------------
# Display all cricket venues that have a seating capacity of more than 50,000 spectators.
# Show venue name, city, country, and capacity. Order by largest capacity first.

# CSV approach

df_SQL4 = pd.read_csv(r'C:\Users\AISHWARYA\PycharmProjects\PythonProject\PythonCourse\Cricbuzz_livetstats\venues.csv')
# print(df_SQL4)

# # --- Database Setup ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'database': 'cricbuzz',
    'password': 'Anvikkevin@123'
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
print("Connected to DB")

# # Create table with unique constraint
cursor.execute("""
    CREATE TABLE IF NOT EXISTS venues (
        venue VARCHAR(255),
        city VARCHAR(40),
        country VARCHAR(35),
        capacity INT
    )
""")
conn.commit()
# print("Table created successfully")

cursor.execute("TRUNCATE TABLE venues")
conn.commit()

# # Insert data in venues:
for index, row in df_SQL4.iterrows():
    cursor.execute("""
        INSERT INTO venues (venue, city, country, capacity)
        VALUES (%s, %s, %s, %s)
    """, (row['venue'], row['city'], row['country'], row['capacity']))

conn.commit()
# print("Data inserted successfully")

# # Query and display results
cursor.execute("""
    SELECT venue, city, country, capacity
    FROM venues
    ORDER BY capacity DESC
""")

results = cursor.fetchall()
q4 = pd.DataFrame(results, columns=['Venue Name', 'City', 'Country', 'Capacity'])
# print(q4)

#  -------------------------------------------------------------------------
# Question 5
# --------------------------------------------------------------------------

# CSV approach

df_SQL5 = pd.read_csv(r'C:\Users\AISHWARYA\PycharmProjects\PythonProject\PythonCourse\Cricbuzz_livetstats\Highest team wins.csv')
# print(df_SQL5)

# # # --- Database Setup ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'database': 'cricbuzz',
    'password': 'Anvikkevin@123'
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
# print("Connected to DB")

# print(df_SQL5.columns)

# Create Table Highest wins by team
cursor.execute("""
    CREATE TABLE IF NOT EXISTS team_wins (
        team VARCHAR(70),
        matches_played INT,
        won INT,
        lost INT
    )
""")

conn.commit()
# print("Table created successfully")

cursor.execute("TRUNCATE TABLE team_wins")
conn.commit()

# Insert data in team_wins:
for index, row in df_SQL5.iterrows():
    cursor.execute("""
        INSERT INTO team_wins (team, matches_played, won, lost)
        VALUES (%s, %s, %s, %s)
    """, (row['Team'], row['Matches Played'], row['Won'], row['Lost']))

conn.commit()
# print("Data inserted successfully")
#
# # Query and display results
cursor.execute("""
    SELECT team, matches_played, won, lost
    FROM team_wins
    ORDER BY won DESC
""")

results = cursor.fetchall()
q5 = pd.DataFrame(results, columns=['Team', 'Matches Played', 'Won', 'Lost'])
# print(q5)

# -----------------------------------------------------------------------------------------
# Question 6
# -------------------------------------------------------------------------------------------

# API used matches/get-Team


url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/35878/team/9"

headers = {
	"x-rapidapi-key": "667adf478dmsh3388b2ca3f77dd6p1c646cjsne88d8510fdff",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
data_SQL6 = (response.json())
# print(data_SQL6)

# Extract player lists from API response
playing_xi = data_SQL6['player'][0]['player']
bench_players = data_SQL6['player'][1]['player']

# Combine all players
all_players = playing_xi + bench_players

# Convert to DataFrame
df_SQL6 = pd.DataFrame(all_players)

# Normalize role names
df_SQL6['role'] = df_SQL6['role'].replace({
    'Batting Allrounder': 'Allrounder',
    'Bowling Allrounder': 'Allrounder'
})

# Count players per role
role_count = df_SQL6.groupby('role').size().reset_index(name='count')

# Database Setup
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_roles (
        role VARCHAR(40),
        count INT
    )
""")

cursor.execute("TRUNCATE TABLE player_roles")

# Insert dynamic values
for idx, row in role_count.iterrows():
    cursor.execute("""
        INSERT INTO player_roles (role, count)
        VALUES (%s, %s)
    """, (row['role'], int(row['count'])))

conn.commit()

cursor.execute("SELECT role, count FROM player_roles ORDER BY count DESC")
results = cursor.fetchall()

q6 = pd.DataFrame(results, columns=["Role", "Count"])
# print(q6)

'''all_players = data_SQL6['player']['playing XI']+data_SQL6['players']['bench']
# print("player keys:",all_players[0].keys())

# Dataframe all_players
df_SQL6= pd.DataFrame(all_players)
df_SQL6['role']= df_SQL6['role'].replace({'Batting Allrounder': 'Allrounder',
                                          'Bowling Allrounder': 'Allrounder'
})
 # Group by roel count
role_count = df_SQL6.groupby('role').size().reset_index(name='count')
# print(role_count)

# --- Database Setup ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'database': 'cricbuzz',
    'password': 'Anvikkevin@123'
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
# print("Connected to DB")

cursor.execute("""TRUNCATE TABLE player_roles""")

# Create a table player_roles
cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_roles (
               role VARCHAR(40),
               count INT
    )
""")

# Dataframe results
role_count = pd.DataFrame({
    'role': ['Allround', 'Batsman', 'WK-Batsman', 'Bowler'],
    'count': [3, 4, 3, 5]
})

# Insert data
for index, row in role_count.iterrows():
    cursor.execute("""
        INSERT INTO player_roles (role, count)
        VALUES (%s, %s)
    """, (row['role'], row['count']))

conn.commit()
# print("Data inserted successfully")

# # Query and display results
cursor.execute("""
    SELECT role, count
    FROM player_roles
    ORDER BY count DESC
""")

results = cursor.fetchall()
q6 = pd.DataFrame(results, columns=['Role','Count'])
# print(q6)'''

# -----------------------------------------------------------------------------------
# Question 7
# -----------------------------------------------------------------------------------


# CSV approach

df_SQL7 = pd.read_csv(r'C:\Users\AISHWARYA\PycharmProjects\PythonProject\PythonCourse\Cricbuzz_livetstats\Highest_runs.csv')
# print(df_SQL7)

# --- Database Setup ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'database': 'cricbuzz',
    'password': 'Anvikkevin@123'
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
# print("Connected to DB")

cursor.execute("""
                CREATE TABLE IF NOT EXISTS format_records (
                match_format VARCHAR(20),
                player_name VARCHAR(30),
                highest_runs INT
                )
""")

cursor.execute("""TRUNCATE TABLE format_records""")

for index, row in df_SQL7.iterrows():
    cursor.execute("""
        INSERT INTO format_records (match_format, player_name, highest_runs)
        VALUES (%s, %s, %s)
    """, (row['Match Format'], row[' Player name'],  (row[' Highest runs'])))

conn.commit()
# print("Data inserted successfully")

# # Query and display results
cursor.execute("""
    SELECT match_format, player_name, highest_runs
    FROM format_records
    # ORDER BY count DESC
""")

results = cursor.fetchall()
q7 = pd.DataFrame(results, columns=['Match Format','Player Name', 'Highest Runs'])
# print(q7)

# -----------------------------------------------------------------------------------
# Question 8
# -----------------------------------------------------------------------------------
#CSV approach

df_SQL8=pd.read_csv(r'C:\Users\AISHWARYA\PycharmProjects\PythonProject\PythonCourse\Cricbuzz_livetstats\series.csv')
# print(df_SQL8)
df_SQL81=pd.read_csv(r'C:\Users\AISHWARYA\PycharmProjects\PythonProject\PythonCourse\Cricbuzz_livetstats\matches.csv')
df_SQL81 = df_SQL81.drop_duplicates(subset=['series_id', 'match_type'])
# print(df_SQL81)

# --- Database Setup ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'database': 'cricbuzz',
    'password': 'Anvikkevin@123'
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
print("Connected to DB")


# cursor.execute("DROP TABLE series_CON")
# cursor.execute("DROP TABLE series")

# Create a table Series
cursor.execute("""
    CREATE TABLE IF NOT EXISTS series (
               series_id INT PRIMARY KEY,
               series_name VARCHAR(100),
               host_country VARCHAR(50),
               start_date DATE
    )
""")
print("Success")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS series_CON (
        match_id INT AUTO_INCREMENT PRIMARY KEY,
        series_id INT,
        match_type VARCHAR(20),
        matches_planned INT,
        FOREIGN KEY (series_id) REFERENCES Series(series_id),
        UNIQUE(series_id, match_type)
    )
""")
print("Success")

# Insert into series table
for index, row in df_SQL8.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO series (series_id, series_name, host_country, start_date)
        VALUES (%s, %s, %s, STR_TO_DATE(%s, '%%d-%%m-%%Y'))
    """, (row['series_id'], row['series_name'], row['host_country'], row['start_date']))

# Insert into series_CON table
for index, row in df_SQL81.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO series_CON (series_id, match_type, matches_planned)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE matches_planned = VALUES(matches_planned)
    """, (row['series_id'], row['match_type'], row['matches_planned']))
conn.commit()
print("Success")

# Query
cursor.execute("""
    SELECT
        s.series_name,
        s.host_country,
        sc.match_type,
        s.start_date,
        sc.matches_planned
    FROM series s
        JOIN series_CON sc ON s.series_id = sc.series_id
        WHERE YEAR(s.start_date) = 2024
""")
results = cursor.fetchall()

q8 = pd.DataFrame(results, columns=["Series Name", "Host Country", "Match Type", "Start Date", "Matches Planned"])
# print(q8)

# -----------------------------
# Database Config
# -----------------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Anvikkevin@123',  # 🔑 update this
    'database': 'cricbuzz'
}

# -----------------------------
# Beginner Level Questions (1–8)
# -----------------------------
SQL_QUESTIONS = {
    "Question 1: Find all players who represent India. Display their full name, playing role, batting style, and bowling style.": """
    SELECT name AS full_name, role AS playing_role, batting_style, bowling_style
    FROM players
""",

    "Question 2: Show all cricket matches that were played in the last few days. Include the match description, both team names, venue name with city, and the match date. Sort by most recent matches first.": """SELECT description, team1_name, team2_name, venue_name, city, match_date
    FROM matches
    ORDER BY match_date DESC
    """,

    "Question 3: List the top 10 highest run scorers in ODI cricket. Show player name, total runs scored, batting average, and number of centuries. Display the highest run scorer first.": """
    SELECT player_name, matches, innings, runs, avg
    FROM top_odi_scorers
    ORDER BY runs DESC
    LIMIT 10
""",

    "Question 4: Display all cricket venues that have a seating capacity of more than 50,000 spectators. Show venue name, city, country, and capacity. Order by largest capacity first.": """
    SELECT venue, city, country, capacity
    FROM venues
    ORDER BY capacity DESC
""",

    "Question 5: Calculate how many matches each team has won. Show team name and total number of wins. Display teams with most wins first.": """
    SELECT team, matches_played, won, lost
    FROM team_wins
    ORDER BY won DESC
""",

    "Question 6: Count how many players belong to each playing role (like Batsman, Bowler, All-rounder, Wicket-keeper). Show the role and count of players for each role.": """
    SELECT role, count
    FROM player_roles
    ORDER BY count DESC
""",

    "Question 7: Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I). Display the format and the highest score for that format.": """
    SELECT match_format, player_name, highest_runs
    FROM format_records
    # ORDER BY count DESC
""",

    "Question 8: Show all cricket series that started in the year 2024. Include series name, host country, match type, start date, and total number of matches planned.": """
SELECT
    s.series_name,
    s.host_country,
    sc.match_type,
    s.start_date,
    sc.matches_planned
FROM series s
JOIN series_CON sc ON s.series_id = sc.series_id
WHERE YEAR(s.start_date) = 2024
""",
}

# -----------------------------
# Execute query and return DataFrame
# -----------------------------
def execute_query(query):
    try:
        conn = pymysql.connect(**DB_CONFIG)
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# -----------------------------
# Page Function
# -----------------------------
def sql_queries_page():
    st.title("📊 SQL Queries - Beginner Level")

    # Predefined response for Questions
    q1 = "These are all the players who represent India. Displaying full name, role, batting style, and bowling style."
    q2 = "These are the recently played matches with description, both team names, venue name with city, and the match date"
    q3 = "These are the top run scorers in ODI format"
    q4 = "These are the Cricket stadiums with highest capacity around the world"
    q5 = "The total number of wins for each team"
    q6 = "These are the player types for the team England"
    q7 = "Players with Highest runs in each format"
    q8 = "List of series and details started in the year 2024"

    question = st.selectbox(
        "Select a Beginner Level Question",
        list(SQL_QUESTIONS.keys())
    )

    st.markdown(f"**Selected Question:** {question}")

    if st.button("Run Query"):
        query = SQL_QUESTIONS[question]
        result_df = execute_query(query)

        if not result_df.empty:
            st.subheader("✅ Query Result")
            st.dataframe(result_df, use_container_width=True)

            if question.startswith("Question 1"):
                st.success(f"✅ Found {len(result_df)} players representing India.")
                st.info(q1)  # ✅ Display the predefined response stored in `q1`

            elif question.startswith("Question 2"):

                st.success(f"✅ Found {len(result_df)} recent matches around the globe.")
                st.info(q2)  # Show the description text

            elif question.startswith("Question 3"):

                st.success(f"✅ The Top {len(result_df)} highest run scorers in ODI Cricket.")
                st.info(q3)  # Show the description text

            elif question.startswith("Question 4"):

                st.success(f"✅ The largest {len(result_df)} cricket stadiums in the world.")
                st.info(q4)  # Show the description text

            elif question.startswith("Question 5"):

                st.success(f"✅ The total number of wins for {len(result_df)} team in cricket.")
                st.info(q5)  # Show the description text

            elif question.startswith("Question 6"):

                # st.success(f"✅ The {len(result_df)} team England in cricket.")
                st.info(q6)  # Show the description text

            elif question.startswith("Question 7"):

                # st.success(f"✅ The {len(result_df)} team England in cricket.")
                st.info(q7)  # Show the description text

            elif question.startswith("Question 8"):

                # st.success(f"✅ The {len(result_df)} team England in cricket.")
                st.info(q8)  # Show the description text
