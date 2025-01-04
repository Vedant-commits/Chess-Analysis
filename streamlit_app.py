import streamlit as st 
import pandas as pd
import plotly.express as px

# Load the Cleaned Data
df = pd.read_csv('./chess_games_raw.csv')

st.title('Chess Data Analysis Dashboard')

# Display the DataSet
st.header("Dataset OverView")
st.write(df.head())

# Popular Opening
st.header('Most Popular Opening')

popular_opening = df['Opening'].value_counts().head(10)
fig_openings = px.bar(
    popular_opening,
    title = "Top 10 Most Popular Opening",
    labels={"index":'Opening', 'value':'GamesPlayed'}
)
st.plotly_chart(fig_openings)

#Elo Trend 
st.header('Elo Trend Over Games')
df['GameNumber'] = range(1,len(df) + 1)
elo_trend = df.groupby('GameNumber')['AverageElo'].mean()
fig_elo_trend = px.line(
    elo_trend.rolling(window=50).mean(),
    title="Elo Trend Over Games",
    labels={"index": "Game Number", "value": "Average Elo"}
)
st.plotly_chart(fig_elo_trend)

# Win Rates by Opening
st.header("Win Rates by Opening")
opening_success = df.groupby('Opening')['Result'].value_counts(normalize=True).unstack()
opening_success['WhiteWinRate'] = opening_success.get('1-0', 0)
opening_success['BlackWinRate'] = opening_success.get('0-1', 0)
opening_success = opening_success[['WhiteWinRate', 'BlackWinRate']].head(10)
fig_win_rates = px.bar(
    opening_success,
    title="Win Rates by Opening",
    labels={"index": "Opening", "value": "Win Rate"},
    barmode="group"
)
st.plotly_chart(fig_win_rates)


# Time Control Analysis
st.header("Time Control Analysis")
time_control_data = df['TimeControl'].value_counts().head(10)
fig_time_control = px.bar(
    time_control_data,
    title="Most Common Time Controls",
    labels={"index": "Time Control", "value": "Games Played"},
    text_auto=True
)
st.plotly_chart(fig_time_control)

# Player Comparison
st.header("Player Comparison")
players = df['White'].unique().tolist()
player_1 = st.selectbox("Select Player 1", players)
player_2 = st.selectbox("Select Player 2", players)

if player_1 and player_2:
    player_1_data = df[(df['White'] == player_1) | (df['Black'] == player_1)]
    player_2_data = df[(df['White'] == player_2) | (df['Black'] == player_2)]
    
    st.write(f"Games Played by {player_1}: {len(player_1_data)}")
    st.write(f"Games Played by {player_2}: {len(player_2_data)}")





# Filtering Options
st.header("Filter Games by Elo and Time Control")
elo_range = st.slider("Select Elo Range", int(df['AverageElo'].min()), int(df['AverageElo'].max()), (1200, 2400))
time_control = st.selectbox("Select Time Control", df['TimeControl'].unique())

filtered_data = df[(df['AverageElo'] >= elo_range[0]) & (df['AverageElo'] <= elo_range[1])]
if time_control:
    filtered_data = filtered_data[filtered_data['TimeControl'] == time_control]

st.write(f"Filtered Data: {len(filtered_data)} games found.")
if st.checkbox("Show Filtered Data"):
    st.write(filtered_data)

