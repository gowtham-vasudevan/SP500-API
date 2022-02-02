# Installing the mysql connector
pip install mysql-connector-python-rf

# Importing the required libraries
import requests
import time
import numpy as np
import pandas as pd
import mysql.connector

# Alpha Vantage API key
alpha_vantage_api_key = 'BQD3V3F1RBV81E53'

# Reading text file containing symbols of S&P 500 companies
with open('S&P500.txt') as f:
    companies = f.read().splitlines()

#Creating pandas dataframe for each database to alter add to mysql database
overview_dataframe = pd.DataFrame(columns=['Symbol', 'Name', 'Sector', 'Industry', 'Market Cap', 'Profit Margin', 'PE Ratio', 'Book Value', 'Dividend Per Share', 'EPS'])

all_stocks = {}
for i in companies:
     all_stocks["{}".format(i)]=pd.DataFrame(columns=['Id', 'Dates', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume'])


# Database details
database_name  = 'stockdatabase'
passwd = 'apiproject'
hostname = 'stockdatabase.cfsievxwcano.us-east-1.rds.amazonaws.com'
port = 3306
user_name = 'admin'

# Connect to the databse
try:
    mydb = mysql.connector.connect(host=hostname, user=user_name,password=passwd)
    cursor = mydb.cursor(buffered=True)
except:
    print("Can't Establish connection to the Companies Database.")
    
    
# Function to add data to the dataframe
def add_to_overview_dataframe(res):
    row = {'Symbol': res['Symbol'], 'Name': res['Name'], 'Sector': res['Sector'], 'Industry': res['Industry'],
        'Market Cap': res['MarketCapitalization'], 'Profit Margin': res['ProfitMargin'], 'PE Ratio': res['PERatio'],
        'Book Value': res['BookValue'], 'Dividend Per Share': res['DividendPerShare'], 'EPS': res['EPS']}
    overview_dataframe = overview_dataframe.append(row, ignore_index=True)
    
    
# Functin to create mysql database using mysql connector
def create_overview_database():
    cursor.execute('USE Companies;')

    cursor.execute("""CREATE TABLE Overview(
            Symbol VARCHAR(7) PRIMARY KEY,
            Name VARCHAR(30),
            Sector VARCHAR(30),
            Industry VARCHAR(30),
            MarketCapitalisation FLOAT(2),
            ProfitMargin FLOAT(2),
            PERatio FLOAT(2),
            BookValue FLOAT(2),
            DividendPerShare FLOAT(2),
            EPS FLOAT(2)
        );""")
    
    
# Insert the values into the database
def insert_into_overview_database(df):
    cursor.execute('USE Companies;')
    for i,j in df.iterrows():
        cursor.execute(f"""INSERT INTO Overview VALUES('{str(j[0])}', '{str(j[1])}', '{str(j[2])}', '{str(j[3])}', {float(j[4])}, {float(j[5])}, {float(j[6])}, {float(j[7])}, {float(j[8])}, {float(j[9])});""")
        

for symbol in companies[0:499]:
    try:
        response = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={sym}&apikey={alpha_vantage_api_key}').json()
        if len(response) == 0:
            print(f'Request returned empty for {symbol}.')
            time.sleep(15)
        else:
            print(f'Successfull request for {symbol}.')
            add_to_overview_dataframe(response)
            print(f'Data appended to Overview Dataframe for {symbol}.')
            time.sleep(15)
    except:
        print(f'Error requesting data for {symbol}.')
        time.sleep(15)



try:
    insert_into_overview_database(overview_dataframe)
except:
    print('Error addinng data to the Overview Database.')
    

    
