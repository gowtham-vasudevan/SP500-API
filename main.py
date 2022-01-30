import requests
import time
import pandas as pd


alpha_vantage_api_key = 'BQD3V3F1RBV81E53'

with open('S&P500.txt') as f:
    companies = f.read().splitlines()


overview_dataframe = pd.DataFrame(columns=['Symbol', 'Name', 'Sector', 'Industry', 'Market Cap', 'Profit Margin', 'PE Ratio', 'Book Value', 'Dividend Per Share', 'EPS'])

all_stocks = {}
for i in companies:
     all_stocks["{}".format(i)]=pd.DataFrame(columns=['Id', 'Dates', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume'])


for symbol in companies:
    try:
        response = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={alpha_vantage_api_key}').json()
        if len(response) == 0:
            print(f'No data to append to the DataFrame for {symbol}.')
            time.sleep(30)
            continue
        print(f'Preparing {symbol} data to add into dataframe.')
        row = {'Symbol': response['Symbol'], 'Name': response['Name'], 'Sector': response['Sector'], 'Industry': response['Industry'],
           'Market Cap': response['MarketCapitalization'], 'Profit Margin': response['ProfitMargin'], 'PE Ratio': response['PERatio'],
           'Book Value': response['BookValue'], 'Dividend Per Share': response['DividendPerShare'], 'EPS': response['EPS']}
        overview_dataframe = overview_dataframe.append(row, ignore_index=True)
        print(f'Added data for {symbol} to the dataframe.')
        time.sleep(30)
    except:
        print(f'Error getting/adding data for {symbol}.')
        time.sleep(30)
        
        
   for symbol in all_stocks.keys():
    try:
        response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={alpha_vantage_api_key}').json()
        if len(response) == 0:
            print(f'No data to get from the {symbol} API.')
            time.sleep(30)
            continue
        print(f'Preparing to ppend DataFrame for {symbol}.')
        for date in response['Time Series (Daily)']:
            row = {'Id':1, 'Dates': date, 'Symbol':symbol, 'Open': response['Time Series (Daily)'][str(date)]['1. open'], 'High': response['Time Series (Daily)'][str(date)]['2. high'], 'Low': response['Time Series (Daily)'][str(date)]['3. low'], 'Close': response['Time Series (Daily)'][str(date)]['4. close'], 'Volume': response['Time Series (Daily)'][str(date)]['5. volume']}
            all_stocks[symbol] = all_stocks[symbol].append(row, ignore_index=True)
            print(f'Added data for {symbol} to the dataframe.')
            time.sleep(30)
    except:
        print(f'Error getting/adding data for {symbol}')
        time.sleep(30)
