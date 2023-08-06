from arcticdb import Arctic
from utils import ticker_to_yf
import streamlit as st
import yfinance as yf
import pandas as pd
import click


INTERVAL = "1h"
PERIOD = "1d"
TICKERS = ["AAPL", "GOOG", "TSLA"]
for i, ticker in enumerate(TICKERS):
    TICKERS[i] = ticker_to_yf(ticker)

for ticker in TICKERS:
    data = ticker.history(period=PERIOD, interval=INTERVAL)
    st.write(f"Volume data for {ticker.info['longName']} for {PERIOD}")
    st.line_chart(data['Volume'])


@click.command()
@click.option("--arg", default="no args", help="Test argument")
def etl(arg):
    print(f"The pipeline was run with {arg}")