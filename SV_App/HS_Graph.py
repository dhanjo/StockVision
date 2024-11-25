import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

# Stock symbols and time range
stocks = ['RELIANCE.BO', 'MRF.NS', 'TATAMOTORS.NS', 'HDFCBANK.NS', 'JINDALSTEL.NS']
start_date = '2024-11-15'
end_date = '2024-11-20'

# Fetch data, plot, and save graphs
for stock in stocks:
    # Download stock data
    data = yf.download(stock,period="5d")
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Close'], label=f'{stock} Closing Prices', color='blue')
    plt.title(f'{stock} Stock Prices (Last 5 Days)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    # plt.show()

    # Save the graph as an image
    file_name = f"{stock}_graph.png"
    plt.savefig(file_name)
    print(f"Graph saved as {file_name}")
    plt.close()