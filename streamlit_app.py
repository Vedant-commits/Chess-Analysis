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
st.title("Chess Opening Effectiveness")
st.write(
    """
    Welcome to the Chess Opening Effectiveness Dashboard!
    This app allows you to analyze chess openings based on their popularity, success rates, and usage patterns across different skill levels.
    Use the filters and interactive charts to explore chess openings and improve your strategies.
    """
)

#Filter by ELO bracket
st.header('Filter Opening by skill bracket')
st.write(
    """
    Use the dropdown menu below to select a skill bracket (e.g., Beginner, Intermediate).
    The app will filter the data to show insights specific to players in the selected bracket.
    """
)
elo_bracket = st.selectbox('Select Elo Bracket',
df['EloBracket'].unique(),index=0)
filtered_data = df[df['EloBracket']==elo_bracket]

#Popular openings
st.header(f"Popular Openings for {elo_bracket} Players")
st.write(
    """
    This chart shows the top 10 most popular chess openings for players in the selected skill bracket.
    Popular openings are determined based on how frequently they are used in games.
    """
)
popular_openings = filtered_data['Opening'].value_counts().head(10)
fig_popular_openings = px.bar(
    popular_openings,
    title=f"Top 10 Most Popular Openings for {elo_bracket} Players",
    labels={"index":"Opening","value":"Games Played"},
    text_auto=True
)
st.plotly_chart(fig_popular_openings)

# Win Rates by Opening

st.header(f"Openning Success Rates for {elo_bracket} Players")
st.write(
    """
    This chart analyzes the success rates of the top 10 chess openings based on their win rates.
    Success rates are calculated separately for White (1-0) and Black (0-1) outcomes.
    Use this chart to identify openings that have historically been effective for players in the selected skill bracket.
    """
)
opening_success = filtered_data.groupby('Opening')['Result'].value_counts(normalize = True).unstack()
opening_success['WhiteWinRate'] = opening_success.get('1-0',0)
opening_success['BlackWinRate'] = opening_success.get('0-1',0)
opening_success = opening_success[['WhiteWinRate','BlackWinRate']].sort_values(by ='WhiteWinRate',
ascending = False).head(10)

fig_opening_win_rates = px.bar(
    opening_success,
    title=f"Top 10 Openings by Win Rate for {elo_bracket} Players",
    barmode='group',
    text_auto=True
)
st.plotly_chart(fig_opening_win_rates)

# Treemap for Openings by Frequency
st.header(f"Opening Frequency for {elo_bracket} Players")
st.write(
    """
    The treemap below visualizes the frequency of chess openings used by players in the selected skill bracket.
    Each tile represents an opening, with larger tiles indicating higher usage.
    """
)
fig_treemap = px.treemap(
    filtered_data,
    path=['Opening'],
    title=f"Opening Frequency Treemap for {elo_bracket} Players",
    color=filtered_data['Opening'].map(filtered_data['Opening'].value_counts()),
    color_continuous_scale='viridis'
)
st.plotly_chart(fig_treemap)



# Time Control Analysis
st.write(
    """
    This section explores the relationship between game length, player skill, and outcomes.
    Use the interactive filters and visualizations to gain insights into how these factors interact.
    """
)

st.header("Filter by Time Control")
time_control_options = df['TimeControl'].unique()
selected_time_control = st.selectbox("Select Time Control",time_control_options,index=0)
filtered_data = df[df['TimeControl']== selected_time_control]

st.write(f"Analyzing games with time control : **{selected_time_control}")

#scatter plot
st.header('Move Count vs Average Elo')
st.write(
    """
    This scatter plot shows the relationship between the number of moves in a game and the average Elo rating of the players.
    Use this to explore how player skill influences game length.
    """
)
fig_scatter = px.scatter(
    filtered_data,
    x='AverageElo',
    y='MoveCount',
    title='Move Count vs Average Elo',
    labels={'AverageElo':'Average Elo',"MoveCount":'Move Count'},
    color='Result',
    hover_data=['White','Black','Result']
)
st.plotly_chart(fig_scatter)

# HeatMap : Game Length by Elo Bracket

st.header("Heatmap of Game Length by Elo Bracket")
st.write(
    """
    The heatmap below shows the most common game lengths for each Elo bracket.
    Darker colors represent higher frequencies.
    """
)

heatmap_data = filtered_data.groupby(['EloBracket','MoveCount']).size().reset_index(name='Frequency')
fig_heatmap = px.density_heatmap(
    heatmap_data,
    x='MoveCount',
    y='EloBracket',
    z= 'Frequency',
    title='Heatmap of the Game Length by Elo Bracket',
    labels={'MoveCount':'Game Length (Number of Moves)', 'EloBracket': 'Elo Bracket'},
    color_continuous_scale='Viridis'
)
st.plotly_chart(fig_heatmap)

# Histogram : Game Length Distribution by Time Control

st.header("Game Length Distribution by Time Control")
st.write(
    """
    This histogram visualizes the distribution of game lengths for the selected time control.
    Use it to understand how game durations vary within different time formats (e.g., Blitz, Rapid, Classical).
    """
)
fig_histogram = px.histogram(
    filtered_data,
    x='MoveCount',
     title=f"Game Length Distribution for {selected_time_control} Games",
      labels={"MoveCount": "Game Length (Number of Moves)", "count": "Frequency"},
    nbins=20,
    color_discrete_sequence=['teal']
)
st.plotly_chart(fig_histogram)



# Player Comparison
# Ensure this file is in your working directory

# Add a GameNumber column if not already present
if "GameNumber" not in df.columns:
    df['GameNumber'] = range(1, len(df) + 1)

# Streamlit app title
st.title("Chess Player Performance Comparison Dashboard")

# Description
st.markdown("""
### Welcome to the Chess Player Performance Comparison Dashboard!

This interactive dashboard is designed to help you explore and compare the performance of chess players based on game data. Whether you're analyzing trends, looking at win rates, or diving into detailed player statistics, this tool provides a comprehensive and visual way to understand player performance.

---

### What You Can Do Here:

#### 1. Compare Chess Players
- Use the dropdown menus to select two players from the dataset.
- The dashboard will display key metrics and visualizations for both players side-by-side.

#### 2. View Key Metrics
- **Games Played**: See how many games each player has participated in.
- **Win Rates**: Discover each player’s win percentage, giving insight into their overall success.

#### 3. Visualize Player Statistics
- **Win Distribution**:
  - Pie charts showcase the breakdown of wins, losses, and draws for each player.
- **Elo Trends**:
  - A dynamic line chart shows the players' average Elo ratings over time, helping you understand how their performance has evolved.

---

### Why Use This Dashboard?
This tool is perfect for:
- **Chess Enthusiasts**: Compare favorite players or analyze game results.
- **Coaches & Analysts**: Study performance trends and strengths of players.
- **Casual Users**: Explore the dataset interactively and learn about player statistics.

Dive into the data, explore the charts, and gain insights into the fascinating world of chess performance!
""")


# Player Selection
st.header("Compare Players")
players = df['White']._append(df['Black']).unique().tolist()  # Combine unique players from White and Black
player_1 = st.selectbox("Select Player 1", players)
player_2 = st.selectbox("Select Player 2", players)

if player_1 and player_2:
    # Filter data for Player 1 and Player 2
    player_1_data = df[(df['White'] == player_1) | (df['Black'] == player_1)]
    player_2_data = df[(df['White'] == player_2) | (df['Black'] == player_2)]

    # Games played
    player_1_games = len(player_1_data)
    player_2_games = len(player_2_data)

    st.subheader(f"Games Played")
    st.write(f"{player_1}: {player_1_games}")
    st.write(f"{player_2}: {player_2_games}")

    # Win Rates
    player_1_win_rate = round(
        len(player_1_data[player_1_data['Result'] == '1-0']) / player_1_games * 100, 2
    )
    player_2_win_rate = round(
        len(player_2_data[player_2_data['Result'] == '0-1']) / player_2_games * 100, 2
    )

    st.subheader("Win Rates")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"{player_1} Win Rate: {player_1_win_rate}%")
    with col2:
        st.write(f"{player_2} Win Rate: {player_2_win_rate}%")

    # Pie Charts for Win Rates
    # Pie Charts for Win Rates
col1, col2 = st.columns(2)
with col1:
    player_1_results = player_1_data['Result'].value_counts()
    fig1 = px.pie(
        player_1_results,
        values=player_1_results.values,
        names=player_1_results.index,
        title=f"{player_1}'s Win Distribution",
    )
    st.plotly_chart(fig1, key="player_1_pie")

with col2:
    player_2_results = player_2_data['Result'].value_counts()
    fig2 = px.pie(
        player_2_results,
        values=player_2_results.values,
        names=player_2_results.index,
        title=f"{player_2}'s Win Distribution",
    )
    st.plotly_chart(fig2, key="player_2_pie")

# Calculate Elo Trends
player_1_elo_trend = player_1_data.groupby('GameNumber')['AverageElo'].mean()
player_2_elo_trend = player_2_data.groupby('GameNumber')['AverageElo'].mean()


# Performance Trends (Average Elo over games)
st.subheader("Performance Trends")
fig3 = px.line(
    x=player_1_elo_trend.index,
    y=player_1_elo_trend.values,
    title=f"{player_1} vs. {player_2}: Elo Trend",
    labels={"x": "Game Number", "y": "Average Elo"},
)
fig3.add_scatter(
    x=player_2_elo_trend.index,
    y=player_2_elo_trend.values,
    mode="lines",
    name=player_2,
)
st.plotly_chart(fig3, key="elo_trend_chart")

st.write(
    """
    This tool allows you to explore chess openings with filters for win rates, skill brackets, or time controls.
    Learn about popular and lesser-known openings and their performance across different scenarios.
    """
)



# Filter by Elo Bracket and Time Control
st.header("Filter Openings by Elo Bracket and Time Control")
elo_bracket = st.selectbox("Select Elo Bracket", df['EloBracket'].unique(), index=0, key="elo_bracket_select")
time_control = st.selectbox("Select Time Control", df['TimeControl'].unique(), index=0, key="time_control_select")

# Filter the dataset based on user input
filtered_data = df[(df['EloBracket'] == elo_bracket) & (df['TimeControl'] == time_control)]
st.write(f"Showing data for **{elo_bracket}** players in **{time_control}** games.")

# Popular Openings Bar Chart
st.header(f"Popular Openings for {elo_bracket} Players")
popular_openings = filtered_data['Opening'].value_counts().head(10)
fig_popular_openings = px.bar(
    popular_openings,
    title=f"Top 10 Most Popular Openings for {elo_bracket} Players",
    labels={"index": "Opening", "value": "Games Played"},
    text_auto=True
)
st.plotly_chart(fig_popular_openings, key="popular_openings_chart")

# Win Rates by Opening Bar Chart
st.header(f"Opening Success Rates for {elo_bracket} Players")
opening_success = filtered_data.groupby('Opening')['Result'].value_counts(normalize=True).unstack()
opening_success['WhiteWinRate'] = opening_success.get('1-0', 0) * 100
opening_success['BlackWinRate'] = opening_success.get('0-1', 0) * 100
opening_success = opening_success[['WhiteWinRate', 'BlackWinRate']].sort_values(by='WhiteWinRate', ascending=False).head(10)

fig_opening_win_rates = px.bar(
    opening_success,
    title=f"Top 10 Openings by Win Rate for {elo_bracket} Players",
    barmode='group',
    text_auto=True,
    labels={"value": "Win Rate (%)", "Opening": "Opening"}
)
st.plotly_chart(fig_opening_win_rates, key="opening_win_rates_chart")

# Tree Diagram for Opening Variations
st.header(f"Opening Frequency for {elo_bracket} Players")
fig_tree = px.treemap(
    filtered_data,
    path=['Opening'],
    title=f"Opening Frequency Treemap for {elo_bracket} Players",
    color=filtered_data['Opening'].map(filtered_data['Opening'].value_counts()),
    color_continuous_scale='viridis'
)
st.plotly_chart(fig_tree, key="opening_variations_treemap")

# Dropdown for Specific Openings
st.header("Select Specific Opening")
available_openings = filtered_data['Opening'].unique()
selected_opening = st.selectbox("Choose an Opening", available_openings, key="opening_select")

if selected_opening:
    opening_data = filtered_data[filtered_data['Opening'] == selected_opening]

    st.subheader(f"Analysis for Opening: {selected_opening}")

    # Win Rates for Selected Opening
    win_rates = opening_data['Result'].value_counts(normalize=True) * 100
    fig_win_rates = px.pie(
        win_rates,
        values=win_rates.values,
        names=win_rates.index,
        title=f"Win Rates for {selected_opening}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_win_rates, key="selected_opening_win_rates")

    # Player Statistics for the Opening
    top_white_players = opening_data['White'].value_counts().head(5)
    top_black_players = opening_data['Black'].value_counts().head(5)

    st.subheader("Top Players Using This Opening")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Top White Players")
        st.table(top_white_players)
    with col2:
        st.write("Top Black Players")
        st.table(top_black_players)


