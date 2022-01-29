# Stock-Price-Prediction

**Project Overview:**

* Created a model that estimates the price of a stock accurately by x%.
* Got data from API using python. {DONE}
* Created a Micro Database instance on AWS and stored the data using python. - {IN PROGRESS: 60%}
* Performed Data Analysis and analysed trends in the data. - {}
* Deployed the model using Flask. {}


This is my first project where I intend to cover the whole data science lifecycle from getting the data from an API, storing the data in a cloud database (AWS), performing data analysis and try to predict the price of the stock a day, week or a month from now based on the requirement of the user.

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

I created a micro database instance in AWS where I store the data and retrieve it whenever required for the model or analysis





**Note:**

This is still a work in progress . I intend on completing within Feb 2022.
