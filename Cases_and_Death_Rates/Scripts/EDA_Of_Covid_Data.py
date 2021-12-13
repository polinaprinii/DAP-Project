import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from IPython.display import clear_output
import pymongo


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

df1.drop(['_id'], axis=1, inplace=True)
df2.drop(['_id'], axis=1, inplace=True)

# Plot global cases in a bar chart
# Create List of date Values
date_list = df1.columns.tolist()[11:]
print(date_list[0], date_list[-1])


# Top 10 countries with the highest numbers of confirmed cases Globally.

print('The top 10 Countries in Cases to Date are: \n',
      df1[['Country/Region', date_list[-1]]].sort_values(by=date_list[-1], ascending=False).head(10))

# Top 10 countries with the highest number of deaths Globally.

print('The top 10 Countries in Deaths to Date are: ',
      df2[['Country/Region', date_list[-1]]].sort_values(by=date_list[-1], ascending=False).head(10))

# Creating Bar Charts to show the top 20 countries in Cases for Each Date
# time.sleep(3)
# for d in date_list:
#     clear_output(wait=True)
#     top_20_per_d = df1.groupby('Country/Region')[['Country/Region', d]].sum().sort_values(by=d, ascending=False).head(20)
#     top_20_per_d.plot(kind='barh', log=True, figsize=(8,6))
#     plt.ylabel("Country/Region", labelpad=14)
#     plt.xlabel("# of Confirmed Cases (log=True)", labelpad=14)
#     plt.title("Chart the confirmed cases per country/region", y=1.02)
#     plt.show()
#     time.sleep(1)

### Bar Graph showing Cumalative Confirmed Cases By Date For The United States

dates = df1.columns.tolist()[11:]
cases_to_date = df1.iloc[255,11:]
plt.bar(dates, cases_to_date)
plt.xticks(dates, size=8)
plt.locator_params(axis='x', nbins=9)
plt.xlabel('Dates (01/29/20 - 12/07/21)')
plt.ylabel('Confirmed Cases to Date')
plt.title('Cases To Date for United States')

plt.show()


### Bar Graph to show total Confirmed Cases Worldwide by Date, To Date
# Adding a row to sum daily global values.
df1 = df1.append(df1.sum(numeric_only=True), ignore_index=True)
totals = df1.iloc[-1,11:]

plt.bar(dates, totals)
plt.xticks(dates, size=8)
plt.locator_params(axis='x', nbins=9)
plt.xlabel('Dates (01/29/20 - 12/07/21)')
plt.ylabel('Total Global Confirmed Cases to Date')
plt.title('Total Global Confirmed Cases By Date')
plt.show()

