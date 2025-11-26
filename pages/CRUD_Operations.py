

import streamlit as st
import pymysql
import pandas as pd

# Database config
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Anvikkevin@123",
    "database": "cricbuzz"
}

# ---------------------------------------------
# DB Connection Helper
# ---------------------------------------------
def get_connection():
    return pymysql.connect(**DB_CONFIG)


# ---------------------------------------------
# Ensure Table Exists (NEW)
# ---------------------------------------------
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS custom_players (
            player_id INT AUTO_INCREMENT PRIMARY KEY,
            player_name VARCHAR(100),
            country VARCHAR(100),
            matches_played INT,
            runs_scored INT,
            batting_avg FLOAT
        )
    """)
    conn.commit()
    conn.close()


# ---------------------------------------------
# CRUD Page
# ---------------------------------------------
def crud_operation_page():

    create_table()      # NEW → Auto-create table
    st.title("🛠️ Player Database — CRUD Operations")

    st.markdown("---")

    # ---------------------------------------------
    # SECTION 1 — ADD NEW PLAYER (BRAND NEW UI)
    # ---------------------------------------------
    st.subheader("➕ Add Player")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Player Name")
        country = st.text_input("Country")

    with col2:
        matches = st.number_input("Matches Played", min_value=0, step=1)
        runs = st.number_input("Total Runs", min_value=0, step=1)
        avg = st.number_input("Batting Average", min_value=0.0, step=0.1)

    if st.button("Add Player", use_container_width=True):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO custom_players (player_name, country, matches_played, runs_scored, batting_avg)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, country, matches, runs, avg))
        conn.commit()
        conn.close()
        st.success(f"✔️ '{name}' added successfully!")
        st.rerun()

    st.markdown("---")

    # ---------------------------------------------
    # SECTION 2 — VIEW ALL PLAYERS
    # ---------------------------------------------
    st.subheader("📋 Player List")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM custom_players", conn)
    conn.close()

    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # ---------------------------------------------
    # SECTION 3 — UPDATE PLAYER (IMPROVED UI)
    # ---------------------------------------------
    st.subheader("✏️ Update Player")

    if not df.empty:

        player_ids = df["player_id"].tolist()
        selected_id = st.selectbox("Select Player", player_ids)

        selected = df[df["player_id"] == selected_id].iloc[0]

        st.markdown("### Editing Details for:")
        st.info(f"**{selected['player_name']}** ({selected['country']})")

        u1, u2 = st.columns(2)

        with u1:
            new_name = st.text_input("Player Name", selected["player_name"])
            new_country = st.text_input("Country", selected["country"])

        with u2:
            new_matches = st.number_input("Matches", 0, value=int(selected["matches_played"]))
            new_runs = st.number_input("Runs", 0, value=int(selected["runs_scored"]))
            new_avg = st.number_input("Average", 0.0, value=float(selected["batting_avg"]))

        if st.button("Update Player", type="primary", use_container_width=True):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE custom_players
                SET player_name=%s, country=%s, matches_played=%s,
                    runs_scored=%s, batting_avg=%s
                WHERE player_id=%s
            """, (new_name, new_country, new_matches, new_runs, new_avg, selected_id))
            conn.commit()
            conn.close()

            st.success("✔️ Player updated successfully!")
            st.rerun()

    st.markdown("---")

    # ---------------------------------------------
    # SECTION 4 — DELETE PLAYER (NEW PREVIEW UI)
    # ---------------------------------------------
    st.subheader("🗑️ Delete Player")

    if not df.empty:

        del_id = st.selectbox("Select Player to Delete", df["player_id"].tolist(), key="delete_picker")
        player = df[df["player_id"] == del_id].iloc[0]

        st.error(f"⚠️ You are about to delete: **{player['player_name']}** from **{player['country']}**")

        if st.button("Delete Player", use_container_width=True):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM custom_players WHERE player_id=%s", (del_id,))
            conn.commit()
            conn.close()
            st.success("🗑️ Player deleted successfully!")
            st.rerun()
