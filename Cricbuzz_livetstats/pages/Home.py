# Pages/Home.py
import streamlit as st
import pymysql

# url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"
#
# querystring = {"statsType":"mostRuns"}
#
# headers = {
# 	"x-rapidapi-key": "667adf478dmsh3388b2ca3f77dd6p1c646cjsne88d8510fdff",
# 	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
# }
#
# response = requests.get(url, headers=headers, params=querystring)
# data=(response.json())
# print(data)
#
# import pymysql
# DB_CONFIG = {
#     'host':'localhost',
#     'user':'root',
#     'database': 'cricbuzz',
#     'password':'Anvikkevin@123'
# }
#
# conn = pymysql.connect( ** DB_CONFIG)
# cursor = conn. cursor()
# print("Connected to DB")
#
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS most_runs_stats (
#         player_id INT PRIMARY KEY,
#         player_name VARCHAR(100),
#         matches INT,
#         innings INT,
#         runs INT,
#         average FLOAT
#     )
# """)
# conn.connect()
# print("table created")
#
# url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"
#
# querystring = {"statsType":"mostRuns"}
#
# headers = {
# 	"x-rapidapi-key": "667adf478dmsh3388b2ca3f77dd6p1c646cjsne88d8510fdff",
# 	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
# }
#
# response = requests.get(url, headers=headers, params=querystring)
# data=(response.json())
#
# # Step 4: Insert each player into DB
# count = 0
# for player in data['values']:
#     row = player['values']
#     try:
#         player_id = int(row[0])
#         name = row[1]
#         matches = int(row[2])
#         innings = int(row[3])
#         runs = int(row[4])
#         avg = float(row[5])
#
#         cursor.execute("""
#             INSERT INTO most_runs_stats (player_id, player_name, matches, innings, runs, average)
#             VALUES (%s, %s, %s, %s, %s, %s)
#             ON DUPLICATE KEY UPDATE
#             player_name = VALUES(player_name),
#             matches = VALUES(matches),
#             innings = VALUES(innings),
#             runs = VALUES(runs),
#             average = VALUES(average)
#             """, (player_id, name, matches, innings, runs, avg) )
#         count += 1
#     except Exception as e:
#         print(f"A Error inserting {row[1]}: {e}")
#
# conn.commit()
# print(f" Done! Inserted {count} players.")
# df = pd.read_sql("SELECT * FROM most_runs_stats ORDER BY runs DESC", conn)
# conn.close()
#
# st.title("🏏 Most Runs Stats - Cricbuzz")
# st.dataframe(df)


# Database config (update if needed)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Anvikkevin@123',  # change if different
    'database': 'cricbuzz'
}

def home_page():
    st.title("🏏 Cricbuzz LiveStats Dashboard")
    st.markdown(
        """
        Welcome to the **Cricbuzz LiveStats Dashboard**! 🎉  

        Navigate using the sidebar:  
        - 📊 **Live Matches** → See live scores and match details  
        - 🗄 **SQL Queries** → Run predefined cricket database queries  

        ---
        """
    )

    # Try to connect and fetch summary stats
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Fetch summary counts
        cursor.execute("SELECT COUNT(*) FROM teams;")
        total_teams = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM players;")
        total_players = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM venues;")
        total_venues = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM matches;")
        total_matches = cursor.fetchone()[0]

        conn.close()

        # Show stats in 4 columns
        st.subheader("📊 Project Database Overview")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Teams", total_teams)
        col2.metric("Players", total_players)
        col3.metric("Venues", total_venues)
        col4.metric("Matches", total_matches)

    except Exception as e:
        st.warning("⚠️ Could not connect to database. Please check DB setup.")
        st.error(f"Error: {e}")
