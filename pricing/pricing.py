import yfinance as yf
import datetime

def get_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    return df

def calculate_best_price(df):
    avg_price = df['Close'].mean()
    max_price = df['Close'].max()
    min_price = df['Close'].min()

    return avg_price, max_price, min_price

def advise(avg_price, max_price, min_price, current_price):
    if current_price < avg_price:
        return f"The current price is below average. You might want to consider buying. Current: {current_price}, Average: {avg_price}"
    elif current_price > avg_price:
        return f"The current price is above average. You might want to consider selling. Current: {current_price}, Average: {avg_price}"

def get_advice(ticker, start_date=datetime.datetime(2023, 1, 1), end_date=datetime.datetime(2023, 6, 1)):
    df = get_stock_data(ticker, start_date, end_date)
    avg_price, max_price, min_price = calculate_best_price(df)
    current_price = df['Close'][-1]
    return advise(avg_price, max_price, min_price, current_price)