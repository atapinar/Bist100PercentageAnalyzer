import datetime as dt
import pandas as pd
import yfinance as yf
import pytz
import plotly.graph_objects as go
import plotly.io as pio

# Make `end` timezone-aware and set start to the beginning of the year
end = dt.datetime.now(pytz.UTC)
start = dt.datetime(end.year, 1, 1, tzinfo=pytz.UTC)  # Start from January 1st of the current year
print(f"Data Range: {start} to {end}")

# Ask the user for a list of stock symbols (comma-separated)
user_input = input("Enter stock symbols separated by commas (e.g., VAKKO, DOCO, FROTO, SASA): ")
stocklist = [symbol.strip().upper() for symbol in user_input.split(',')]
stocks = [i + ".IS" for i in stocklist]  # Adjust for Turkish stocks on Yahoo Finance

print(f"Selected Stocks: {stocks}")

# Use yfinance directly to download the data from the start of the year
df = yf.download(stocks, start=start, end=end)

# Check if data was retrieved
if df.empty:
    print("No data retrieved. Please check your stock symbols.")
else:
    # Access the 'Close' prices
    if 'Close' in df:
        close = df['Close']
    else:
        close = df

    # Calculate YTD percentage change
    ytd_change = ((close.iloc[-1] - close.iloc[0]) / close.iloc[0]) * 100
    print("YTD Percentage Change:")
    print(ytd_change)

    # Plot using Plotly online mode
    fig = go.Figure()

    # Add a bar for each stock's YTD percentage change
    for stock_symbol, original_name in zip(stocks, stocklist):
        if stock_symbol in close.columns:
            fig.add_trace(go.Bar(
                x=[original_name],  # Display stock name
                y=[ytd_change[stock_symbol]],
                name=original_name  # Use the original name provided by the user for clarity
            ))
        else:
            print(f"Skipping {original_name} as no data is available.")

    # Update layout for better visualization
    fig.update_layout(
        title='Year-to-Date (YTD) Percentage Change for Selected Stocks',
        xaxis_title='Stock Symbol',
        yaxis_title='YTD Percentage Change (%)',
        legend_title='Stock Symbol',
        template='plotly_dark',
        width=1200,
        height=800
    )

    # Display the interactive plot online
    # This line will open the chart in your browser and upload to Plotly's website if logged in
    pio.show(fig)