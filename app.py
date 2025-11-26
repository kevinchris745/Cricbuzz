import streamlit as st
from pages import Home, Live_Matches, sql_queries, CRUD_Operations, Top_Player_Stats

# Configure Streamlit page
st.set_page_config(
    page_title="🏏 Cricbuzz LiveStats",
    page_icon=":cricket_bat_and_ball:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.selectbox(
    "Select a Page",
    ["Home", "Live Matches", "Top Player stats", "SQL Queries", "CRUD Operations"]
)

# Route to selected page
if page == "Home":
    Home.home_page()

elif page == "Live Matches":
    Live_Matches.live_matches_page()

elif page == "SQL Queries":
    sql_queries.sql_queries_page()

elif page == "Top Player stats":
    Top_Player_Stats.top_player_stats_page()

elif page == "CRUD Operations":
    CRUD_Operations.crud_operation_page()
