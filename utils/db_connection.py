import pymysql
import streamlit as st

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Anvikkevin@123',  # 🔑 User name
    'database': 'cricbuzz'
}

def create_connection():
    """Create and return a database connection."""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None
