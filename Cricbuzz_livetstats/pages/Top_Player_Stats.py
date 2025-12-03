import streamlit as st
import pandas as pd
import pymysql

# --- Database Connection ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'database': 'cricbuzz',
    'password': 'Anvikkevin@123'
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

# --- Fetcher function ---
def fetch_table(table_name):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


# ============================
#     STREAMLIT PAGE UI
# ============================
def top_player_stats_page():

    st.title("🏏 Top Player Statistics")

    st.write("Choose which dataset you want to view:")

    option = st.selectbox(
        "Available Data Sources:",
        [
            "Most Runs (SQL)",
            "Format Records (SQL)",
            "Most Wickets (SQL)"
        ]
    )

    # --- Show correct table ---
    if option == "Most Runs (SQL)":
        st.subheader("📌 Most Runs")
        try:
            df = fetch_table("most_runs_stats")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error reading most_runs_stats: {e}")

    elif option == "Format Records (SQL)":
        st.subheader("📌 Format Records")
        try:
            df = fetch_table("format_records")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error reading format_records: {e}")

    elif option == "Most Wickets (SQL)":
        st.subheader("📌 Most Wickets")
        try:
            df = fetch_table("wickets")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error reading wickets: {e}")

