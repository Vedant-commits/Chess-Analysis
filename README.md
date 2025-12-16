Chess Player Performance Analyzer
A comprehensive Python tool for analyzing chess games with detailed performance metrics, temporal trends, and game duration analysis.
🚀 Quick Start
Prerequisites

Python 3.8 or higher
pip package manager

Installation

Clone the repository

bashgit clone <repository-url>
cd chess-analyzer

Create a virtual environment (recommended)

bash# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install required dependencies

bashpip install -r requirements.txt
Verifying Installation
Run this command to verify all dependencies are installed:
bashpython -c "import pandas, numpy, chess, plotly, matplotlib; print('✅ All core dependencies installed successfully!')"
📦 Dependencies
Core Requirements

pandas (≥1.5.0): Data manipulation and analysis
numpy (≥1.24.0): Numerical computations
python-chess (≥1.999): PGN file processing
plotly (≥5.14.0): Interactive visualizations
matplotlib (≥3.6.0): Static plotting

Optional Dependencies

kaleido (≥0.2.1): Export charts as PNG/SVG/PDF
pillow (≥9.3.0): Image processing
jupyter: For notebook interface

🔧 Troubleshooting
Import Errors
If you encounter import errors, ensure all dependencies are installed:
bashpip install --upgrade -r requirements.txt
Kaleido Issues (for image export)
If image export fails:
bash# Uninstall and reinstall kaleido
pip uninstall kaleido
pip install kaleido==0.2.1
Chess Module Not Found
If python-chess import fails:
bashpip install python-chess --upgrade
💻 Usage
Using Jupyter Notebook
bashjupyter notebook chess_analyzer.ipynb
Using Python Script
pythonfrom chess_analyzer import ChessPlayerAnalyzer
import pandas as pd

# Load your data
df = pd.read_csv('chess_games.csv')

# Initialize analyzer
analyzer = ChessPlayerAnalyzer(df)

# Analyze a player
analysis = analyzer.analyze_player('PlayerName')
Data Input Options

CSV File: Place your chess_games_raw.csv in the project directory
PGN File: Use the process_pgn_to_dataframe() function:

pythondf = process_pgn_to_dataframe('your_games.pgn')
📊 Features

Performance Analysis: Win rates, streaks, improvement trends
Game Duration Analysis: Statistical distribution, patterns by result
Temporal Trends: Rating progression over actual dates
Opening Analysis: Performance by opening choice
Export Options: HTML, PNG, SVG, PDF formats

📁 Project Structure
chess-analyzer/
├── chess_analyzer.ipynb     # Main Jupyter notebook
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── chess_games_raw.csv    # Your chess data (not included)
└── reports/               # Generated reports directory
    ├── *.html            # Interactive HTML reports
    ├── *.png             # Static image exports
    └── batch_summary.csv # Batch analysis results
🐛 Known Issues

Kaleido on M1 Macs: May require special installation

bash   pip install kaleido --platform macosx_11_0_arm64

Large PGN Files: Processing may be slow for files >100MB

Consider using num_games parameter to limit processing
