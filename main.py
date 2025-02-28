import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def load_data(filepath):
    # Load CSV data, convert 'time' to datetime, and add useful time columns
    data = pd.read_csv(filepath)
    data['time'] = pd.to_datetime(data['time'])
    data.sort_values('time', inplace=True)
    data['hour'] = data['time'].dt.hour
    data['date'] = data['time'].dt.date
    # Mark the Asian session (00:00 to 08:00) for later calculations.
    data['session'] = data['hour'].apply(lambda h: 'asian session' if 0 <= h < 8 else None)
    return data

def compute_session_levels(data):
    
    # For each date, calculate the high and low during the Asian session 
    # Merge these values back into the main DataFrame and determine the stop-loss level
    
    asian_data = data[data['session'] == 'asian session']
    session_stats = asian_data.groupby('date').agg(
        asian_high=('high', 'max'),
        asian_low=('low', 'min')
    ).reset_index()
    data = data.merge(session_stats, on='date', how='left')
    # Define stop-loss as the midpoint between the Asian session high and low
    data['stoploss'] = data['asian_high'] - (data['asian_high'] - data['asian_low']) / 2
    return data

def plot_candlestick(data):
    # Plot a candlestick chart with Asian session levels and stop-loss overlay
    chart = go.Figure(data=[go.Candlestick(
        x=data['time'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        name='GBPJPY Price'
    )])
    chart.update_layout(
        xaxis_rangeslider_visible=False,
        height=600,
        title_text='GBPJPY Candlestick Chart (Currency: USD)'
    )
    chart.add_trace(go.Scatter(x=data['time'], y=data['asian_high'], name='Asian High'))
    chart.add_trace(go.Scatter(x=data['time'], y=data['asian_low'], name='Asian Low'))
    chart.add_trace(go.Scatter(x=data['time'], y=data['stoploss'], name='Stop Loss'))
    chart.show()

def simulate_trades(data):
    trades = []
    active_trade = None

    for _, row in data.iterrows():
        hr = row['hour']
        # If no trade is active, consider entering a trade during the 8-12 AM window
        if active_trade is None:
            if 8 <= hr < 12:
                if row['open'] > row['asian_high']:
                    active_trade = {
                        'state': 'open',
                        'order_type': 'buy',
                        'open_time': row['time'],
                        'open_price': row['open'],
                        'close_time': None,
                        'close_price': None
                    }
                elif row['open'] < row['asian_low']:
                    active_trade = {
                        'state': 'open',
                        'order_type': 'sell',
                        'open_time': row['time'],
                        'open_price': row['open'],
                        'close_time': None,
                        'close_price': None
                    }
                if active_trade:
                    trades.append(active_trade)
        else:
            # Check exit conditions for an open trade 
            if hr >= 17:
                # Force exit after 5 PM 
                active_trade['state'] = 'closed'
                active_trade['close_time'] = row['time']
                active_trade['close_price'] = row['open']
                active_trade = None
            else:
                if active_trade['order_type'] == 'buy' and row['low'] <= row['stoploss']:
                    active_trade['state'] = 'closed'
                    active_trade['close_time'] = row['time']
                    active_trade['close_price'] = row['stoploss']
                    active_trade = None
                elif active_trade['order_type'] == 'sell' and row['high'] >= row['stoploss']:
                    active_trade['state'] = 'closed'
                    active_trade['close_time'] = row['time']
                    active_trade['close_price'] = row['stoploss']
                    active_trade = None

    return pd.DataFrame(trades)

def calculate_trade_profit(trade):

    conversion_factor = 100000 / 130
    if trade['order_type'] == 'buy':
        profit = (trade['close_price'] - trade['open_price']) * conversion_factor
    else:
        profit = (trade['open_price'] - trade['close_price']) * conversion_factor
    return profit - 10

def plot_performance(trades, initial_capital):
    # Plot the portfolio's evolution over time including the initial investment
    if trades.empty:
        print("No trades were executed.")
        return

    trades['profit'] = trades.apply(calculate_trade_profit, axis=1)
    trades['cumulative_profit'] = trades['profit'].cumsum()
    trades['portfolio_value'] = initial_capital + trades['cumulative_profit']
    trades.sort_values('close_time', inplace=True)

    performance_chart = px.line(
        trades,
        x='close_time',
        y='portfolio_value',
        title=f'Cumulative Portfolio Value (USD) - Initial Investment: ${initial_capital}',
        labels={'close_time': 'Trade Close Time', 'portfolio_value': 'Portfolio Value (USD)'}
    )
    performance_chart.show()

def compute_sharpe_ratio(trades, risk_free_rate=0, annualize=False):
    # Ensure trades are sorted by time
    trades = trades.sort_values('close_time')
    # Compute returns as percentage changes in portfolio value
    returns = trades['portfolio_value'].pct_change().dropna()
    sharpe_ratio = (returns.mean() - risk_free_rate) / returns.std()
    if annualize:
        sharpe_ratio *= (252 ** 0.5)
    return sharpe_ratio

def main():
    data_filepath = 'data.csv'
    initial_capital = 10000
    market_data = load_data(data_filepath)
    market_data = compute_session_levels(market_data)
    trades = simulate_trades(market_data)
    plot_performance(trades, initial_capital)
    
    if not trades.empty:
        sharpe = compute_sharpe_ratio(trades, risk_free_rate=0, annualize=False)
        print(f"Sharpe Ratio: {sharpe:.2f}")
    else:
        print("No trades executed; cannot compute Sharpe Ratio.")

if __name__ == '__main__':
    main()