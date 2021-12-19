import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from IPython.display import clear_output
import pymongo
from pyecharts.charts import Map, Geo
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import webbrowser

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

# df1 = df1.append(df1.sum(numeric_only=True), ignore_index=True)
# total_cases = df1.iloc[-1, 11:]
#
# df2 = df2.append(df2.sum(numeric_only=True), ignore_index=True)
# total_deaths = df2.iloc[-1, 11:]

# Making world map

countries_cases = list(df1['Country/Region'])
totalcases = list(df1.iloc[0:, -1])

covid_data = [[countries_cases[i], totalcases[i]] for i in range(len(countries_cases))]
covid_map = Map(init_opts=opts.InitOpts(width="1000px", height="460px"))
covid_map.add('Total Confirmed Cases',
              covid_data,
              maptype='world',
              is_map_symbol_show=False)
covid_map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
covid_map.set_global_opts(
    visualmap_opts=opts.VisualMapOpts(max_=1100000, is_piecewise=True, pieces=[
        {"min": 500000},
        {"min": 200000, "max": 499999},
        {"min": 100000, "max": 199999},
        {"min": 50000, "max": 99999},
        {"min": 10000, "max": 49999},
        {"max": 9999}, ]),
    title_opts=opts.TitleOpts(
        title='Total Global Confirmed Covid-19 Cases',
        subtitle='As Of ' + most_recent_date,
        pos_left='center',
        padding=0,
        item_gap=2,  # gap between title and subtitle
        title_textstyle_opts=opts.TextStyleOpts(color='darkblue',
                                                font_weight='bold',
                                                font_family='Courier New',
                                                font_size=30),
        subtitle_textstyle_opts=opts.TextStyleOpts(color='grey',
                                                   font_weight='bold',
                                                   font_family='Courier New',
                                                   font_size=13)),
    legend_opts=opts.LegendOpts(is_show=False))
covid_map.render('A:\College\DAP-Project\Cases_and_Death_Rates\Visualizations\covid_today_world_map.html')

# Automatically opens the html file containing the interactive map
webbrowser.open_new_tab('A:\College\DAP-Project\Cases_and_Death_Rates\Visualizations\covid_today_world_map.html')

# Bar Graph Showing top 20 Countries in Deaths
top_20_deaths = df2.groupby("Country/Region")[['Country/Region', date_list[-1]]].sum().sort_values(by=date_list[-1],
                                                                                                   ascending=False).head(
    20)
top_20_deaths.plot(kind='barh', log=True, figsize=(8, 6))
plt.gca().invert_yaxis()
plt.ylabel("Country/Region", labelpad=14)
plt.xlabel("Number of Deaths to Date (log=True)", labelpad=14)
plt.title("Countries with The Highest Number of Deaths to Date", y=1.02)
plt.savefig('A:\College\DAP-Project\Cases_and_Death_Rates\Visualizations\Countries_with_highest_deaths_to_date.png')
plt.show()

# Bar Graph Showing top 20 Countries in Confirmed Cases
top_20_cases = df1.groupby('Country/Region')[['Country/Region', date_list[-1]]].sum().sort_values(by=date_list[-1],
                                                                                                  ascending=False).head(
    20)
top_20_cases.plot(kind='barh', log=True, figsize=(8, 6))
plt.gca().invert_yaxis()
plt.ylabel("Country/Region", labelpad=14)
plt.xlabel("Number of Confirmed Cases to Date (log=True)", labelpad=14)
plt.title("Countries with The Highest Number of Confirmed Cases to Date", y=1.02)
plt.savefig('A:\College\DAP-Project\Cases_and_Death_Rates\Visualizations\Countries_with_highest_cases_to_date.png')
plt.show()
