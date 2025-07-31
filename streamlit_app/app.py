import streamlit as st
import pandas as pd

st.set_page_config(page_title="IPL Analytics Pro", layout="wide")
st.title("🏏 IPL Analytics Dashboard")

@st.cache_data
def load_data():
    matches = pd.read_csv("IPL Dataset/matches.csv")
    deliveries = pd.read_csv("IPL Dataset/deliveries.csv")
    home_away = pd.read_csv("IPL Dataset/teamwise_home_and_away.csv")
    return matches, deliveries, home_away

matches, deliveries, home_away = load_data()

st.sidebar.title("📊 Choose Analysis")
option = st.sidebar.radio(
    "Select one:",
    [
        "🏠 Overview Dashboard",
        "👥 Team-wise Stats",
        "🔥 Best Finishers (Death Overs)",
        "⚔️ Player Comparison",
        "🎲 Toss vs Match Winner",
        "🏟️ Home vs Away Performance"
    ]
)

# 1. Overview
if option == "🏠 Overview Dashboard":
    st.header("Season-wise Overview")
    season_stats = matches.groupby("Season").agg({
        "id": "count",
        "player_of_match": "nunique",
        "winner": "nunique"
    }).rename(columns={"id": "Total Matches", "player_of_match": "Unique MOMs", "winner": "Teams with Wins"})

    st.dataframe(season_stats)

    st.subheader("Top 5 Man of the Match Winners")
    top_mom = matches["player_of_match"].value_counts().head(5)
    st.table(top_mom)

    st.subheader("Most Matches Played by Teams")
    match_counts = pd.concat([matches["team1"], matches["team2"]]).value_counts().head(5)
    st.bar_chart(match_counts)

# 2. Team-wise Stats
elif option == "👥 Team-wise Stats":
    st.header("Team Performance Overview")
    team = st.selectbox("Select a team:", sorted(matches["team1"].unique()))
    played = matches[(matches["team1"] == team) | (matches["team2"] == team)]
    wins = matches[matches["winner"] == team]

    st.markdown(f"**Total Matches Played:** {played.shape[0]}")
    st.markdown(f"**Total Wins:** {wins.shape[0]}")

    st.subheader("Most Frequent Opponents")
    opponents = pd.concat([
        played[played["team1"] == team]["team2"],
        played[played["team2"] == team]["team1"]
    ])
    st.bar_chart(opponents.value_counts().head(5))

# 3. Best Finishers
elif option == "🔥 Best Finishers (Death Overs)":
    st.header("Top Batsmen in Overs 16–20")
    death_overs = deliveries[deliveries["over"] >= 16]
    finishers = death_overs.groupby("batsman")["batsman_runs"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(finishers)

    st.markdown("These are players who consistently finish strong in the death overs (16–20).")

# 4. Player Comparison Tool
elif option == "⚔️ Player Comparison":
    st.header("Compare Two Players – Batting Stats")
    player1 = st.selectbox("Select Player 1", sorted(deliveries["batsman"].unique()))
    player2 = st.selectbox("Select Player 2", sorted(deliveries["batsman"].unique()), index=1)

    def get_batting_stats(player):
        df = deliveries[deliveries["batsman"] == player]
        total_runs = df["batsman_runs"].sum()
        balls = df.shape[0]
        strike_rate = (total_runs / balls) * 100 if balls > 0 else 0
        return pd.Series([total_runs, balls, round(strike_rate, 2)],
                         index=["Runs", "Balls", "Strike Rate"])

    stats = pd.DataFrame({
        player1: get_batting_stats(player1),
        player2: get_batting_stats(player2)
    })

    st.table(stats)

# 5. Toss vs Match Winner
elif option == "🎲 Toss vs Match Winner":
    st.header("Toss Winner = Match Winner?")
    matches["same"] = matches["toss_winner"] == matches["winner"]
    toss_stats = matches["same"].value_counts(normalize=True) * 100

    st.write(f"✅ Toss winners won the match **{round(toss_stats.get(True, 0), 2)}%** of the time.")
    st.write(f"❌ Toss winners lost the match **{round(toss_stats.get(False, 0), 2)}%** of the time.")
    st.bar_chart(toss_stats)

# 6. Home vs Away
elif option == "🏟️ Home vs Away Performance":
    st.header("Team-wise Home vs Away Win %")
    home_away_sorted = home_away.sort_values("home_win_percentage", ascending=False)
    st.dataframe(home_away_sorted)

    st.subheader("Top 5 Home Dominators")
    st.bar_chart(home_away_sorted.set_index("team")["home_win_percentage"].head(5))