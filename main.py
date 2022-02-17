# Importing the required libraries
import requests
import time
import numpy as np
import pandas as pd
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine


# For creating the database
def create_database():
    conn = sqlite3.connect('Companies.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE Overview(
            Symbol VARCHAR(7) PRIMARY KEY,
            Name VARCHAR(30),
            Sector VARCHAR(30),
            Industry VARCHAR(30),
            'Market Cap' FLOAT(2),
            'Profit Margin' FLOAT(2),
            'PE Ratio' FLOAT(2),
            'Book Value' FLOAT(2),
            'Dividend Per Share' FLOAT(2),
            EPS FLOAT(2)
        );""")
    conn.commit()
    conn.close()


# Insert values to the Overview table 
def add_to_overview_dataframe(res, local_df):
    row = {'Symbol': res['Symbol'], 'Name': res['Name'], 'Sector': res['Sector'], 'Industry': res['Industry'],
        'Market Cap': res['MarketCapitalization'], 'Profit Margin': res['ProfitMargin'], 'PE Ratio': res['PERatio'],
        'Book Value': res['BookValue'], 'Dividend Per Share': res['DividendPerShare'], 'EPS': res['EPS']}
    local_def = local_def.append(row, ignore_index=True)
    return local_df


def get_overview_data_from_api(comp, key, df):
    for symbol in comp[0:498]:
        try:
            response = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={key}').json()
            if len(response) == 0:
                print(f'Request returned empty for {symbol}.')
                time.sleep(15)
            else:
                print(f'Successfull request for {symbol}.')
                df = add_to_overview_dataframe(response, df)
                print(f'Data appended to Overview Dataframe for {symbol}.')
                time.sleep(15)
        except:
            print(f'Error requesting data for {symbol}.')
            time.sleep(15)
    return df


def add_to_sqlite_overview_database(df):
    engine = sqlalchemy.create_engine('sqlite:///Companies.db', echo=False)
    df.to_sql('Overview', con=engine, if_exists='append', index=False)


def add_to_stock_dataframe(local_sym, res, df):
    ind = 1
    for date in res['Time Series (Daily)']:
        row = {'Id': ind, 'Dates': str(date), 'Symbol': str(local_sym), 'Open': float(res['Time Series (Daily)'][str(date)]['1. open']), 'High': float(res['Time Series (Daily)'][str(date)]['2. high']), 'Low': float(res['Time Series (Daily)'][str(date)]['3. low']), 'Close': float(res['Time Series (Daily)'][str(date)]['4. close']), 'Volume': float(res['Time Series (Daily)'][str(date)]['5. volume'])}
        df[local_sym] = df[local_sym].append(row, ignore_index=True)
        ind = ind + 1
    return df


def request_stock_data_from_api(key, stock_details):
    for sym in stock_details.keys():
        try:
            response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={sym}&apikey={key}').json()
            if len(response) == 0:
                print(f'No data to get from the {sym} API.')
                time.sleep(15)
                continue
            print(f'Successfull request for {sym} data.')
            stock_details = add_to_stock_dataframe(sym, response, stock_details)
            print(f'Data appended to the {sym} dataframe.')
            time.sleep(15)
        except:
            print(f'Error adding data to the {sym} dataframe.')

    return stock_details


def add_to_sqlite_stock_database(sym, stock_dict):
    try:
        conn = sqlite3.connect('Companies.db')
        engine = sqlalchemy.create_engine('sqlite:///Companies.db', echo=False)
        stock_dict[sym].to_sql(str(sym), con=engine, if_exists='append', index=False)
        conn.commit()
        conn.close()
    except:
        pass

def main():    
    # Defining all the required variables
    alpha_vantage_api_key = 'BQD3V3F1RBV81E53'

    with open('S&P500.txt') as f:
        companies = f.read().splitlines()

    overview_dataframe = pd.DataFrame(columns=['Symbol', 'Name', 'Sector', 'Industry', 'Market Cap', 'Profit Margin', 'PE Ratio', 'Book Value', 'Dividend Per Share', 'EPS'])

    # Creates a dict of pandas dataframe with stock symbols as keys
    all_stocks = {}
    for i in companies:
        all_stocks["{}".format(i)]=pd.DataFrame(columns=['Id', 'Dates', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume'])


    create_database()
    overview_dataframe = get_overview_data_from_api(companies, alpha_vantage_api_key, overview_dataframe)
    add_to_sqlite_overview_database(overview_dataframe)

    all_stocks = request_stock_data_from_api(alpha_vantage_api_key, all_stocks)
    
    for i in list(all_stocks.keys()):
        add_to_sqlite_stock_database(i, all_stocks)
