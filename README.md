# Chess Player Performance Analyzer

A comprehensive data analysis tool for chess players to improve their game through detailed performance analytics and insights from their historical games.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage Instructions](#usage-instructions)
- [Data Format Specifications](#data-format-specifications)
- [Metrics Explained](#metrics-explained)
- [Output Files](#output-files)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

## Features

- **Individual Player Analysis**: Analyze any player's complete game history
- **Performance Metrics**: Win rates, rating progression, opening success rates
- **Visual Reports**: Interactive HTML dashboards with 6+ chart types
- **Batch Processing**: Analyze multiple players automatically
- **Player Comparison**: Compare performance between different players
- **Improvement Tracking**: Identify trends and progress over time

## Installation

### Requirements
- Python 3.7 or higher
- Operating System: Windows, macOS, or Linux
- Minimum 4GB RAM recommended for large datasets

### Step 1: Clone or Download the Repository
```bash
git clone https://github.com/yourusername/chess-analysis.git
cd chess-analysis
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Libraries
```bash
pip install -r requirements.txt
```

Required packages:
- pandas>=1.3.0
- numpy>=1.20.0
- plotly>=5.0.0
- python-chess>=1.0.0
- streamlit>=1.25.0

### Step 4: Verify Installation
```bash
python -c "import pandas, plotly, chess; print('Installation successful!')"
```

## Usage Instructions

### Option 1: Jupyter Notebook Analysis

1. **Launch Jupyter Notebook**
```bash
   jupyter notebook
```

2. **Open the Analysis Notebook**
   - Navigate to `chess_analysis.ipynb`
   - Click to open

3. **Configure Data Source**
   - In Cell 2, update the file path:
```python
   # For CSV file:
   df = pd.read_csv('your_chess_games.csv')
   
   # For PGN file:
   df = process_pgn_to_dataframe('your_games.pgn', num_games=None)
```

4. **Select Player for Analysis**
   - Run all cells up to Section 6
   - In Section 6, modify the player name:
```python
   PLAYER_NAME = "YourPlayerName"  # Replace with actual player name
```

5. **Generate Analysis**
   - Run remaining cells
   - Reports will be saved as `{player_name}_chess_report.html`

### Option 2: Streamlit Web Application

1. **Prepare Your Data**
   - Place your chess games file as `chess_games_raw.csv` in the project directory

2. **Launch Streamlit App**
```bash
   streamlit run streamlit_app.py
```

3. **Use the Web Interface**
   - Browser will open automatically (or visit http://localhost:8501)
   - Select player from dropdown menu
   - Navigate through analysis tabs
   - Export reports using sidebar options

### Option 3: Command Line Analysis
```python
from chess_analysis import ChessPlayerAnalyzer

# Initialize analyzer
analyzer = ChessPlayerAnalyzer('chess_games_raw.csv')

# List available players
players = analyzer.get_available_players(min_games=10)
print(players)

# Analyze specific player
analysis = analyzer.analyze_player("PlayerName")
fig = analyzer.create_player_report("PlayerName", "output_report.html")
```

## Data Format Specifications

### Input Format: PGN Files

Standard PGN headers expected:
```
[Event "Tournament Name"]
[Site "Location/Platform"]
[Date "2023.01.15"]
[Round "1"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]
[WhiteElo "1650"]
[BlackElo "1600"]
[ECO "B12"]
[Opening "Caro-Kann Defense"]
[TimeControl "300+0"]

1. e4 c6 2. d4 d5 ... {moves}
```

**Required PGN Headers:**
- `White` - White player's name (string)
- `Black` - Black player's name (string)
- `Result` - Game result: "1-0", "0-1", "1/2-1/2", or "*"

**Optional PGN Headers:**
- `Date` - Game date (YYYY.MM.DD format)
- `WhiteElo` - White's rating (integer)
- `BlackElo` - Black's rating (integer)
- `Opening` - Opening name (string)
- `ECO` - ECO opening code (string)
- `TimeControl` - Time format (string)
- `Event` - Tournament/event name (string)

### Input Format: CSV Files

**Required CSV Columns:**
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| White | string | White player name | "JohnDoe" |
| Black | string | Black player name | "JaneSmith" |
| Result | string | Game result | "1-0" |

**Optional CSV Columns:**
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| WhiteElo | integer/float | White's rating | 1650 |
| BlackElo | integer/float | Black's rating | 1600 |
| Date | string/datetime | Game date | "2023-01-15" |
| Opening | string | Opening name | "Sicilian Defense" |
| ECO | string | ECO code | "B90" |
| TimeControl | string | Time control | "300+0" |
| MoveCount | integer | Total moves | 45 |

### Output Format: Processed Data

The tool generates several output files:

**1. chess_analysis_output.csv** - Enhanced dataset with:
- All original columns
- `GameNumber` - Sequential game identifier
- `AverageElo` - Mean of both players' ratings

**2. player_statistics.csv** - Summary statistics:
- `Player` - Player name
- `Total_Games` - Games played
- `Win_Rate` - Win percentage
- `Current_Rating` - Latest rating

**3. {player}_analysis.csv** - Individual player data:
- `PlayerColor` - Color played (White/Black)
- `PlayerResult` - Result from player's perspective
- `Opponent` - Opponent's name
- `PlayerElo` - Player's rating for that game

### Missing Data Handling

| Missing Field | Default Action |
|--------------|----------------|
| Player names | Skip game (required) |
| Result | Use "*" (unfinished) |
| Date | Auto-generate sequential dates |
| Ratings | Store as NaN |
| Opening | Use "Unknown" |
| Time Control | Use "Standard" |
| Move Count | Calculate if possible, else NaN |

## Metrics Explained

### Basic Performance Metrics

**Win Rate**
```
Win Rate = (Number of Wins / Total Games) × 100
```
Example: 48 wins in 100 games = 48% win rate

**Draw Rate**
```
Draw Rate = (Number of Draws / Total Games) × 100
```

**Loss Rate**
```
Loss Rate = (Number of Losses / Total Games) × 100
```

**Points Percentage** (Tournament scoring)
```
Points % = ((Wins + 0.5 × Draws) / Total Games) × 100
```
Example: 48 wins + 20 draws in 100 games = (48 + 0.5×20)/100 = 58%

### Rating Metrics

**Average Elo**
```
Average Elo = (White Elo + Black Elo) / 2
```
Used to categorize game difficulty level

**Rating Change**
```
Rating Change = Current Rating - Starting Rating
```
Positive = improvement, Negative = decline

**Rolling Average** (10-game window)
```
Rolling Avg = Mean of last 10 game ratings
```
Smooths out rating fluctuations

### Opening Performance

**Opening Win Rate**
```
Opening Win Rate = (Wins with Opening / Games with Opening) × 100
```
Calculated separately for each opening

**Opening Points %**
```
Opening Points = ((Wins + 0.5 × Draws) with Opening / Games with Opening) × 100
```

### Improvement Metrics

**Quarterly Performance**
- Games divided into 4 equal quarters (Q1-Q4)
- Q1 = Oldest 25% of games
- Q4 = Most recent 25% of games

**Improvement Trend**
```
Trend = Q4 Win Rate - Q1 Win Rate
```
- Positive = Improving
- Negative = Declining
- Near zero (±2%) = Stable

**Performance vs Opponent Strength**
Games categorized by opponent rating:
- <1200: Beginner
- 1200-1400: Intermediate
- 1400-1600: Advanced
- 1600-1800: Expert
- 1800-2000: Master
- 2000+: Grandmaster level

### Color-Specific Metrics

**White/Black Win Rate**
Calculated separately for games played as each color:
```
White Win Rate = (Wins as White / Games as White) × 100
Black Win Rate = (Wins as Black / Games as Black) × 100
```

## Output Files

| File | Description |
|------|-------------|
| `{player}_chess_report.html` | Interactive visual report |
| `chess_analysis_output.csv` | Processed game data |
| `player_statistics.csv` | All players summary |
| `{player}_games.csv` | Individual player's games |
| `error_log.txt` | Processing errors (if any) |

## Troubleshooting

### Common Issues and Solutions

**Issue: "No games found for player"**
- Check exact spelling of player name (case-sensitive)
- Use `get_available_players()` to see valid names
- Ensure player has minimum required games (default: 10)

**Issue: "FileNotFoundError: chess_games_raw.csv"**
- Ensure data file is in correct directory
- Check file name spelling
- For PGN files, update the file path in code

**Issue: "ValueError: could not convert string to float"**
- Check rating columns contain only numbers
- Remove or fix non-numeric ratings
- Tool will handle as NaN automatically

**Issue: Missing rating progression chart**
- Player may have no games with ratings
- Check if WhiteElo/BlackElo columns exist
- Ratings stored as text need conversion

**Issue: Streamlit app won't start**
```bash
# Try:
pip install --upgrade streamlit
streamlit cache clear
streamlit run streamlit_app.py --server.port 8502
```

## Examples

### Example 1: Analyze Single Player
```python
analyzer = ChessPlayerAnalyzer('chess_games_raw.csv')
analysis = analyzer.analyze_player("Magnus_Carlsen")

print(f"Win Rate: {analysis['overall_stats']['win_rate']:.1f}%")
print(f"Best Opening: {analysis['opening_analysis'].iloc[0]['opening']}")
```

### Example 2: Compare Multiple Players
```python
players = ["Player1", "Player2", "Player3"]
comparison = compare_players(df, players)
print(comparison[['Player', 'Win_Rate', 'Current_Rating']])
```

### Example 3: Batch Generate Reports
```python
top_players = player_stats.head(10)['Player'].tolist()
successful, failed = batch_analyze_players(df, top_players, 'reports/')
```

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review example notebooks in `/examples` directory
3. Create an issue on GitHub
4. Contact: your-email@example.com

## License

MIT License - Feel free to use and modify for your chess improvement journey!
