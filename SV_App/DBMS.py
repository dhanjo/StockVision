import yfinance as yf
import requests
import time
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client['AI']
collection = db['Data_Stock']


# Function to fetch real-time stock data using YFinance
def fetch_realtime_stock_data(symbol):
    stock = yf.Ticker(symbol)
    try:
        stock_info = stock.info
        latest_data=stock.history(period="1d")
        data = {
            'Symbol': symbol,
            'Current Price': stock_info.get('regularMarketPrice'),
            'Volume': stock_info.get('volume'),
            'P/E Ratio': stock_info.get('trailingPE'),
            'Open': stock_info.get('regularMarketOpen'),
            'High': stock_info.get('dayHigh'),
            'Low': stock_info.get('dayLow'),
            'Previous Close': stock_info.get('regularMarketPreviousClose'),
            'Latest Close' : latest_data['Close'].iloc[-1]
        }
        
        return data
    except requests.ConnectionError as e:
        print(f"Connection error: {e}. Retrying in 2 minutes...")
        time.sleep(120)
        return None

# Function to fetch last one hour Google Trends data using SerpApi
def fetch_google_trends_data(query, api_key):
    url = 'https://serpapi.com/search.json'
    params = {
        'engine': 'google_trends',
        'q': query,
        'data_type': 'TIMESERIES',
        'time_range': 'now 1-H',  # Last one hour
        'geo': 'IN',  # India
        'api_key': api_key
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        #print("SerpApi Response:")
        #print(data)
        
        if 'error' in data:
            print(f"Error from SerpApi: {data['error']}")
            return None
        
        timeseries_data = data.get('interest_over_time', {}).get('timeline_data', [])
        if timeseries_data:
            # Extract the latest data point
            latest_data_point = timeseries_data[-1]
            
            # Depending on the data structure, extract the interest value
            if 'value' in latest_data_point:
                # For minute-level data, 'value' is directly available
                interest = int(latest_data_point['value'][0])
                return interest
            elif 'values' in latest_data_point:
                # For other data structures, extract from 'values' list
                values = latest_data_point.get('values', [])
                if values:
                    interest = int(values[0].get('extracted_value', 0))
                    return interest
            else:
                print("Data structure not recognized.")
                return None
        else:
            print("No timeseries data returned.")
            return None
    except Exception as e:
        print(f"Error fetching Google Trends data: {e}")
        return None

# Fetch real-time stock and Google Trends data
def store_data(symbol,query) :
    api_key = 'e2b4af888819490ab23e3f00668602543bbc0203f41d23b424fef17625a3d718'  # Replace with your actual API key

    stock_data = fetch_realtime_stock_data(symbol)
    google_trends_data = fetch_google_trends_data(query, api_key)

    # Store the fetched data
    if stock_data is not None and google_trends_data is not None:
        # print("\nReal-time Stock Data:")
        seardict={"Symbol":stock_data['Symbol']}
        if(collection.find_one(seardict) == None):
            collection.insert_one({
                'Symbol' : stock_data['Symbol'],
                'Open': stock_data['Open'],
                'High': stock_data['High'],
                'Low': stock_data['Low'],
                'P/E Ratio': stock_data['P/E Ratio'],
                'Google Trends':google_trends_data,
                'Price Change' : stock_data['Latest Close'] - stock_data['Previous Close']
            })
            print("Added",symbol, "Data")
        else:
            collection.update_one(
            {"Symbol": stock_data['Symbol']},
            {
                "$set": {
                    'Open': stock_data['Open'],
                    'High': stock_data['High'],
                    'Low': stock_data['Low'],
                    'P/E Ratio': stock_data['P/E Ratio'],
                    'Google Trends':google_trends_data,
                    'Price Change' : stock_data['Latest Close'] - stock_data['Previous Close']
                }
            }
            )
            print("Updated",symbol,"Data")

store_data("TATAMOTORS.NS","TATAMOTORS")
store_data("MRF.NS","MRF")
store_data("RELIANCE.BO","RELIANCE")
store_data("HDFCBANK.NS","HDFCBANK")
store_data("JINDALSTEL.NS","JINDALSTEL")
# if google_trends_data is not None:
#     print("\nReal-time Google Trends Data:")
#     print(f" - Google Trends Interest: {google_trends_data}")
# else:
#     print("\nCould not fetch Google Trends data.")