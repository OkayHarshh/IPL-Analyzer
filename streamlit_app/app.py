import streamlit as st
import pandas as pd

st.set_page_config(page_title="IPL Analytics", layout="centered")
st.title("IPL Analytics Dashboard")

@st.cache_data
def load_data():
    matches = pd.read_csv(r"../IPL-Analyzer/IPL Dataset/matches.csv")
    deliveries = pd.read_csv(r"../IPL-Analyzer/IPL Dataset/deliveries.csv")
    home_away = pd.read_csv(r"../IPL-Analyzer/IPL Dataset/teamwise_home_and_away.csv")

    return matches, deliveries, home_away

matches, deliveries, home_away = load_data()

option = st.sidebar.selectbox(
    "Select Analysis",
    ["Top Run Scorers", "Top Wicket Takers", "Toss vs Match Winner", "Team Wins by Season", "Home vs Away Win %", "Best Finishers (Death Overs)"]
)

if option == "Top Run Scorers":
    st.header("Top 10 Run Scorers")
    top = deliveries.groupby("batsman")["batsman_runs"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top)

elif option == "Top Wicket Takers":
    st.header("Top 10 Wicket Takers")
    wickets = deliveries[deliveries["player_dismissed"].notnull()]
    top = wickets.groupby("bowler").size().sort_values(ascending=False).head(10)
    st.bar_chart(top)

elif option == "Toss vs Match Winner":
    st.header("Toss Winner = Match Winner %")
    matches["same"] = matches["toss_winner"] == matches["winner"]
    result = matches["same"].value_counts(normalize=True) * 100
    st.bar_chart(result)

elif option == "Team Wins by Season":
    season = st.selectbox("Choose Season", sorted(matches["season"].unique(), reverse=True))
    wins = matches[matches["season"] == season]["winner"].value_counts()
    st.bar_chart(wins)

elif option == "Home vs Away Win %":
    st.header("Home vs Away Performance")
    st.dataframe(home_away.sort_values("home_win_percentage", ascending=False))

elif option == "Best Finishers (Death Overs)":
    st.header("Finishers in Overs 16-20")
    df = deliveries[deliveries["over"] >= 16]
    finishers = df.groupby("batsman")["batsman_runs"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(finishers)