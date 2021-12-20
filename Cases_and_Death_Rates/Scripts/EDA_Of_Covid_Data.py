import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import plotly.graph_objects as go
import time
from IPython.display import clear_output
import pymongo
from pyecharts.charts import Map, Geo
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import webbrowser
import pymongo.errors


# This file will handle the exploratory data analysis of the two cleaned files from mongoDB of cases and death

# Read in from MONGODB
try:
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

except pymongo.errors.ConnectionFailure as ConError:
    print("Error while attempting connection to Database")
except pymongo.errors.NetworkTimeout as NetworkTimeoutError:
    print("The Network has Timed out")
else:
    print("Connection Made")
finally:
    print("Data Read Successful")

# Removing _id Column added by MongoDB
df1.drop(['_id'], axis=1, inplace=True)
df2.drop(['_id'], axis=1, inplace=True)

# Changing Country/Region value from "US" To "United States" for interaction with world map graph

df1['Country/Region'] = df1['Country/Region'].replace(['US'], 'United States')
df2['Country/Region'] = df2['Country/Region'].replace(['US'], 'United States')

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
#
df1 = df1.append(df1.sum(numeric_only=True), ignore_index=True)
total_cases = df1.iloc[-1, 11:]

df2 = df2.append(df2.sum(numeric_only=True), ignore_index=True)
total_deaths = df2.iloc[-1, 11:]

# Find maximum infection rate for all of the countries
df1.set_index('Country/Region')
df1_aggregated = df1.groupby('Country/Region').sum().sort_values(by=date_list[-1], ascending=False)
print(df1_aggregated.head())
print(df1_aggregated.index)

countries = list(df1_aggregated.index)
max_case_rates = []
for c in countries:
    max_case_rates.append(df1_aggregated.loc[c].diff().max())

avg_case_rates = []
for d in countries:
    avg_case_rates.append(df1_aggregated.loc[d].diff().mean())

df1_aggregated['max_case_rates'] = max_case_rates
df1_aggregated['avg_case_rates'] = avg_case_rates
print(df1_aggregated.head())

# Isolate max case rate and average case rate
target_data = ['max_case_rates', 'avg_case_rates']
max_and_avg_case_data = pd.DataFrame(df1_aggregated[target_data])
max_and_avg_case_data.reset_index(inplace=True)

# Writing to local CSV
# noinspection PyTypeChecker

max_and_avg_case_data.to_csv(r"A:\College\DAP-Project\Cases_and_Death_Rates\Data\RAW Data for "
                             r"EDA\AVG_MAX_COVID_CASES.csv")

try:
    # Creating a new collection in MongoBD for the new dataframe
    covid_cases_max_and_avg = db.covid_cases_max_and_avg

    # Turning Dataframe into a dict for storage
    max_and_avg_case_data = max_and_avg_case_data.to_dict('records')

    # Sending file to Collections
    Cases_max_avg = covid_cases_max_and_avg.insert_many(max_and_avg_case_data)
except pymongo.errors.CollectionInvalid as invalidColError:
    print("collection invalid")
except pymongo.errors.ConnectionFailure as ConError:
    print("Error while trying to connect to the Database.")
except pymongo.errors.WriteError as writeError:
    print("error while trying to write to Database")
else:
    print("Write to Database successful")
finally:
    print("Files written to Database successfully")


