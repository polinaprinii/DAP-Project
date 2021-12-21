import webbrowser
import matplotlib.pyplot as plt
import pandas as pd
import pymongo
import pymongo.errors

from matplotlib import rcParams
from pyecharts import options as opts
from pyecharts.charts import Map

# This file will handle the data Visualisations of the two cleaned files from mongoDB of cases and death

# Read in from MONGODB
try:
    # Connecting to MongoDB
    client = pymongo.MongoClient('192.168.56.30', 27017)

    # Mongo Database where the cleaned data is stored
    db = client.covid_data

    # Database Collection Names
    covid_cases_clean = db.covid_cases_clean
    covid_deaths_clean = db.covid_deaths_clean
    covid_cases_max_and_avg = db.covid_cases_max_and_avg

    # Pulling records from Mongodb to dataframes
    df1 = pd.DataFrame(list(covid_cases_clean.find()))
    df2 = pd.DataFrame(list(covid_deaths_clean.find()))
    df3 = pd.DataFrame(list(covid_cases_max_and_avg.find()))

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
df3.drop(['_id'], axis=1, inplace=True)

# Changing Country/Region value from "US" To "United States" for interaction with world map graph

df1['Country/Region'] = df1['Country/Region'].replace(['US'], 'United States')
df2['Country/Region'] = df2['Country/Region'].replace(['US'], 'United States')
df3['Country/Region'] = df3['Country/Region'].replace(['US'], 'United States')

# Create List of date Values
date_list = df1.columns.tolist()[11:]

# Setting a Variable to hold the latest date for the data set
most_recent_date = df1.columns[-1]

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
# Save Map Locally as HTML File
covid_map.render(r'A:\College\DAP-Project\Cases_and_Death_Rates\Visualizations\covid_today_world_map.html')

# Automatically opens the html file containing the interactive map
webbrowser.open_new_tab(r'A:\College\DAP-Project\Cases_and_Death_Rates\Visualizations\covid_today_world_map.html')

# Bar Graph Showing top 20 Countries in Deaths
top_20_deaths = df2.groupby(
    "Country/Region")[['Country/Region', date_list[-1]]].sum().sort_values(
    by=date_list[-1], ascending=False).head(20)

top_20_deaths.plot(kind='barh', log=True, figsize=(8, 6))
plt.gca().invert_yaxis()
plt.ylabel("Country/Region", labelpad=14)
plt.xlabel("Number of Deaths to Date (" + most_recent_date + ") (log=True)", labelpad=14)
plt.title("Countries with The Highest Number of Deaths to Date", y=1.02)
plt.savefig(r'A:\College\DAP-Project\Cases_and_Death_Rates\Visualizations\Countries_with_highest_deaths_to_date.png')
plt.show()

# Bar Graph Showing top 20 Countries in Confirmed Cases
top_20_cases = df1.groupby(
    'Country/Region')[['Country/Region', date_list[-1]]].sum().sort_values(
    by=date_list[-1], ascending=False).head(20)

top_20_cases.plot(kind='barh', log=True, figsize=(8, 6))
plt.gca().invert_yaxis()
plt.ylabel("Country/Region", labelpad=14)
plt.xlabel("Number of Confirmed Cases to Date (" + most_recent_date + ") (log=True)", labelpad=14)
plt.title("Countries with The Highest Number of Confirmed Cases to Date " + most_recent_date, y=1.02)
plt.savefig(r'A:\College\DAP-Project\Cases_and_Death_Rates\Visualizations\Countries_with_highest_cases_to_date.png')
plt.show()

# Creating a line graph of the top 10 countries by cases
df1.set_index('Country/Region')
df1_aggregated = df1.groupby('Country/Region').sum().sort_values(by=date_list[-1], ascending=False).head(10)
print(df1_aggregated.head())


for i in df1_aggregated.index:
    df1_aggregated.loc[i].plot()

plt.legend()
plt.title("Number of Confirmed Cases to Date (" + most_recent_date + ")")
plt.ylabel('Cumulative Number of Confirmed Cases')
plt.xlabel('Dates')
plt.savefig(r'A:\College\DAP-Project\Cases_and_Death_Rates\Visualizations\10_highest_countries_Cases_to_date.png')
plt.show()

# Creating a line graph of the top 10 countries by deaths
df2.set_index('Country/Region')
df2_aggregated = df2.groupby('Country/Region').sum().sort_values(by=date_list[-1], ascending=False).head(10)
print(df2_aggregated.head())
print(df2_aggregated.index)

for i in df2_aggregated.index:
    df2_aggregated.loc[i].plot()

plt.legend()
plt.title("Number of Deaths to Date (" + most_recent_date + ")")
plt.ylabel('Cumulative Number of Deaths')
plt.xlabel(Dates)
plt.savefig(r'A:\College\DAP-Project\Cases_and_Death_Rates\Visualizations\10_Highest_countries_deaths_to_date.png')

plt.show()
print(df3.head())

x_axis_values = df3['Country/Region']

# Plot line to compare global Average daily cases vs max daily cases
df3.set_index('Country/Region', inplace=True)
x = df3.index
plt.rcParams["figure.figsize"] = [10, 8]
rcParams.update({'figure.autolayout': True})
df3.plot()
plt.xticks(x=x, rotation=45)
plt.title('Average Daily Cases Vs. Maximum Daily Cases')
plt.xlabel('Countries')
plt.ylabel('Number of Cases')

plt.savefig(r'A:\College\DAP-Project\Cases_and_Death_Rates\Visualizations\Average_vs_Maximum_Daily_Cases.png')
plt.show()
