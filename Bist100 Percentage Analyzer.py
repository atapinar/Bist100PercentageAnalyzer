import datetime as dt
import pandas as pd
import yfinance as yf
import pytz
import plotly.graph_objects as go
import plotly.io as pio

end = dt.datetime.now(pytz.UTC)
start = dt.datetime(end.year, 1, 1, tzinfo=pytz.UTC)

user_input = input("Enter stock symbols separated by commas (e.g., VAKKO, DOCO, FROTO, SASA): ")
stocklist = [symbol.strip().upper() for symbol in user_input.split(',')]
stocks = [i + ".IS" for i in stocklist]

df = yf.download(stocks, start=start, end=end)

if not df.empty:
    if 'Close' in df:
        close = df['Close']
    else:
        close = df

    ytd_change = ((close.iloc[-1] - close.iloc[0]) / close.iloc[0]) * 100

    fig = go.Figure()

    for stock_symbol, original_name in zip(stocks, stocklist):
        if stock_symbol in close.columns:
            fig.add_trace(go.Bar(
                x=[original_name],
                y=[ytd_change[stock_symbol]],
                name=original_name
            ))

    fig.update_layout(
        title='Year-to-Date (YTD) Percentage Change for Selected Stocks',
        xaxis_title='Stock Symbol',
        yaxis_title='YTD Percentage Change (%)',
        legend_title='Stock Symbol',
        template='plotly_dark',
        width=1200,
        height=800
    )

    pio.show(fig)
