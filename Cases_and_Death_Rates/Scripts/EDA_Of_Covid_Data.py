import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from IPython.display import clear_output
import pymongo
from arcgis.gis import GIS

# This file will handle the exploratory data analysis of the two global cases and death files from mongoDB

# Read in from MONGODB
# Connecting to MongoDB
client = pymongo.MongoClient('192.168.56.30', 27017)

# Mongo Database where the cleaned data is stored
db = client.covid_data

# Database Collection Names
covid_cases_clean = db.covid_cases_clean
covid_deaths_clean = db.covid_deaths_clean

# Pulling records from Mongodb to dataframes
df1 = pd.DataFrame(list(covid_cases_clean.find()))
df2 = pd.DataFrame(list(covid_deaths_clean.find()))

# Removing _id Column added by MongoDB
df1.drop(['_id'], axis=1, inplace=True)
df2.drop(['_id'], axis=1, inplace=True)

# Plot global cases in a bar chart
# Create List of date Values
date_list = df1.columns.tolist()[11:]
print(date_list[0], date_list[-1])

# Top 10 countries with the highest numbers of confirmed cases Globally.

print('The top 10 Countries with most Cases to Date are: \n',
      df1[['Country/Region', date_list[-1]]].sort_values(by=date_list[-1], ascending=False).head(10))

# Top 10 countries with the highest number of deaths Globally.

print('The top 10 Countries with most Deaths to Date are: ',
      df2[['Country/Region', date_list[-1]]].sort_values(by=date_list[-1], ascending=False).head(10))

# Setting a Variable to hold the latest date for the data set
most_recent_date = df1.columns[-1]

# Bar Graph showing total Confirmed Cases By Date, to date For The United States
dates_cases = df1.columns.tolist()[11:]
dates_deaths = df2.columns.tolist()[11:]

df1 = df1.append(df1.sum(numeric_only=True), ignore_index=True)
total_cases = df1.iloc[-1, 11:]

df2 = df2.append(df2.sum(numeric_only=True), ignore_index=True)
total_deaths = df2.iloc[-1, 11:]

cases_to_date_US = df1.iloc[255, 11:]
plt.bar(dates_cases, cases_to_date_US, color='red')
plt.xticks(dates_cases, size=8)
plt.locator_params(axis='x', nbins=9)
plt.xlabel('Dates (01/29/20 -' + most_recent_date + ')')
plt.ylabel('Confirmed Cases to Date')
plt.title('Cases To Date for United States')

plt.show()

# Bar Graph to show total Confirmed Cases Worldwide by Date, To Date
# Adding a row to sum daily global values.


plt.bar(dates_cases, total_cases)
plt.xticks(dates_cases, size=8)
plt.locator_params(axis='x', nbins=9)
plt.xlabel('Dates (01/29/20 -' + most_recent_date + ')')
plt.ylabel('Total Global Confirmed Cases to Date')
plt.title('Total Global Confirmed Cases By Date')
plt.show()

plt.bar(dates_deaths, total_deaths, color='red')
plt.xticks(dates_deaths, size=8)
plt.locator_params(axis='x', nbins=9)
plt.xlabel('Dates (01/29/20 -' + most_recent_date + ')')
plt.ylabel('Confirmed Deaths to Date')
plt.title('Deaths To Date for United States')

plt.show()

plt.plot(dates_cases, total_deaths, label='total Deaths', marker='o', linewidth=3)
plt.xlabel('Dates')
plt.ylabel('Number of People')
plt.legend(loc='upper left')
plt.xticks(dates_cases)
plt.title('Deaths Over TIme')
plt.show()


plt.plot(dates_cases, total_cases, label='Total Cases', marker='o', linewidth=3)
plt.xlabel('Dates')
plt.ylabel('Number of People')
plt.legend(loc='upper left')
plt.xticks(dates_cases)
plt.title('Cases over time')
plt.show()


