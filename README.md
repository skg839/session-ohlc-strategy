SessionTrader: A Compounded Forex Trading Simulator

📌 Overview

SessionTrader is a Python-based forex backtesting tool that simulates a session-based trading strategy using historical price data. It focuses on the Asian session, identifying key price levels to trigger trade entries and exits. The strategy dynamically compounds profits, reinvesting capital after each trade. Performance is evaluated using key metrics like cumulative portfolio value and the Sharpe ratio to assess risk-adjusted returns.

🚀 Features

- Session-Based Strategy: Trades based on Asian session highs and lows.
- Automated Backtesting: Uses pandas to process historical forex data.
- Dynamic Compounding: Reinvests capital to simulate realistic portfolio growth.
- Performance Metrics: Calculates Sharpe ratio and cumulative profits.
- Visualizations: Plots price movements, trades, and portfolio growth using Plotly.

📂 Installation & Setup

Requirements:

Ensure you have Python installed along with the necessary dependencies:
```
pip install pandas plotly
```
Clone Repository:
```
git clone https://github.com/yourusername/SessionTrader.git
cd SessionTrader
```
Running the Backtest:
```
python main.py
```
This will execute the strategy on the dataset and display key performance metrics along with visualizations.

⚙️ How It Works:

- Loads Historical Data: Reads a CSV file containing forex price data.
- Identifies Key Levels: Finds the Asian session high and low for trade signals.
- Executes Trades: Opens and closes trades based on strategy conditions.
- Compounds Profits: Reinvests the total portfolio value in each new trade.
- Evaluates Performance: Computes Sharpe ratio and plots portfolio growth.

📊 Example Output:

- Candlestick Chart: Displays price action with session levels.
- Portfolio Growth Chart: Shows cumulative profits over time.
- Sharpe Ratio: Measures risk-adjusted returns.

![newplot](https://github.com/user-attachments/assets/904d1bf6-f0d8-45f9-955f-2e98d8030a3d)

