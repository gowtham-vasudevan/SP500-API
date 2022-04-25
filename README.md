# Stock Data from API

**Project Overview:**

* Get historical prices of all S&P 500 companies from API using python.
* Create an sqlite3 database
* Store the values in the sqlite3 database

**GETTING DATA:**

Using the Alpha Vantage API to get the data of all the S&P 500 companies and store it in a pandas dataframe. The price of the stock were stored in 500 different dataframes and the company oveview of all the 500 companies have their own separate dataframes. In total, we have 506 dataframes. 505 for stock prices and 1 for the company overview.

In the stock price dataframe, we have the following columns:
1. Id
2. Dates
3. Symbol
4. Open
5. high
6. Low
7. Close 
8. Volume

In the company overview dataframe, we have the following columns:
1. Symbol
2. Name
3. Sector
4. Industry
5. Market Capitalisation
6. Profit Margin
7. PE Ratio
8. Book Value
9. Dividend Per Share
10. EPS

**Storing in a Database:**

Created an sqlite3 database and added values to the database.
