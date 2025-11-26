import streamlit as st
import requests

# -----------------------------
# API Config
# -----------------------------
API_URL = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
HEADERS = {
	"x-rapidapi-key": "667adf478dmsh3388b2ca3f77dd6p1c646cjsne88d8510fdff",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

# -----------------------------
# Fetch Live Matches
# -----------------------------
@st.cache_data(ttl=60)  # cache API calls for 1 min to avoid hitting limits
def fetch_live_matches():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API request failed: {e}")
        return None

# -----------------------------
# Helper: Format Scores
# -----------------------------
def format_score(score_obj: dict) -> str:
    """Return formatted cricket score like '120/3 in 15.2 overs'."""
    if not score_obj:
        return "—"
    return f"{score_obj.get('runs', 0)}/{score_obj.get('wickets', 0)} in {score_obj.get('overs', 0)} overs"

# -----------------------------
# Page Renderer
# -----------------------------
def live_matches_page():
    st.title("🏏 Live Matches")

    data = fetch_live_matches()
    if not data or "typeMatches" not in data:
        st.warning("⚠️ No live matches available right now.")
        return

    for type_match in data["typeMatches"]:
        match_type = type_match.get("matchType", "Unknown Format")
        st.subheader(f"📌 {match_type} Matches")

        for series in type_match.get("seriesMatches", []):
            series_info = series.get("seriesAdWrapper", {})
            series_name = series_info.get("seriesName", "Unknown Series")
            matches = series_info.get("matches", [])

            with st.expander(f"🏆 {series_name}", expanded=True):
                for match in matches:
                    match_info = match.get("matchInfo", {})
                    team1 = match_info.get("team1", {}).get("teamName", "TBD")
                    team2 = match_info.get("team2", {}).get("teamName", "TBD")
                    status = match_info.get("status", "No status available")
                    venue = match_info.get("venueInfo", {}).get("ground", "Unknown Venue")

                    # ✅ Extract Scores
                    match_score = match.get("matchScore", {})
                    team1_score = format_score(match_score.get("team1Score", {}).get("inngs1"))
                    team2_score = format_score(match_score.get("team2Score", {}).get("inngs1"))

                    # Card-style display
                    st.markdown(
                        f"""
                        ### {team1} 🆚 {team2}
                        - 🏟️ **Venue:** {venue}  
                        - 📊 **Status:** {status}  
                        - 🔹 **{team1}:** {team1_score}  
                        - 🔹 **{team2}:** {team2_score}  
                        """
                    )