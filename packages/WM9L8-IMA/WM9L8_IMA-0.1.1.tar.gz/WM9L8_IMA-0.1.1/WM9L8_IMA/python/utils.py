import yfinance as yf

def ticker_to_yf(ticker):
    return yf.Ticker(ticker)