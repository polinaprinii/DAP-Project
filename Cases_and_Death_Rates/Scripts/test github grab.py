import io
import pandas as pd
import pycountry
import requests.exceptions
pd.options.mode.chained_assignment = None

########################################################################################################################

# Assigning the correct RAW github Urls to Variables

url1 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url2 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url3 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
url4 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
all_urls = [url1, url2, url3, url4]
# Reading the content of the URL

########################################################################################################################

try:
    download1 = requests.get(url1).content
    download2 = requests.get(url2).content
    download3 = requests.get(url3).content
    download4 = requests.get(url4).content

    # Turning the read content into a pandas dataframe

    df1 = pd.read_csv(io.StringIO(download1.decode('utf-8')))
    df2 = pd.read_csv(io.StringIO(download2.decode('utf-8')))
    df3 = pd.read_csv(io.StringIO(download3.decode('utf-8')))
    df4 = pd.read_csv(io.StringIO(download4.decode('utf-8')))

# exception handling for errors

except requests.exceptions.HTTPError as errhttp:
    print("Http Error:", errhttp)
except requests.exceptions.ConnectionError as errcon:
    print("Error Connecting:", errcon)
except requests.exceptions.Timeout as errtime:
    print("Timeout Error:", errtime)
except requests.exceptions.RequestException as erreq:
    print("Misc Error", erreq)

else:
    # Ensuring each dataframe now contains data and letting user know that the process was successful.
    if df1.size and df2.size and df3.size and df4.size > 0:
        print("data successfully imported and stored in dataframe.")

    # Printing the first 5 rows of each dataframe
finally:
    all_dfs = [df1, df2, df3, df4]
    for i in all_dfs:
        print(i.head(5))

########################################################################################################################

def CountryISOConverter(dataframe):
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3

    codes = [countries.get(country, 'ISO Code Unknown') for country in dataframe['Country/Region']]

    dataframe['iso3'] = codes
    cols1 = dataframe.columns.tolist()
    cols1 = cols1[-1:] + cols1[:-1]
    dataframe = dataframe[cols1]
    return dataframe


df1 = CountryISOConverter(df1)
df2 = CountryISOConverter(df2)


# print(df2.head(), '\n', df1.head(), '\n')


########################################################################################################################


def Combined_Key_Col_Add(dataframe):
    dataframe["Combination_Key"] = dataframe['Country/Region'].str.cat(dataframe['Province/State'], sep=", ")

    Combined_Key_Col = dataframe.pop("Combination_Key")

    dataframe.insert(3, "Combination_Key", Combined_Key_Col)

    return dataframe


df1 = Combined_Key_Col_Add(df1)
df2 = Combined_Key_Col_Add(df2)


########################################################################################################################
def Null_Count(dataframe):
    no_nulls = (dataframe.isnull().sum())

    return print(no_nulls)


def Province_fill(dataframe):

    dataframe['Province/State'].fillna(dataframe['Country/Region'], inplace=True)

    return dataframe

def Combination_fill(dataframe):
    dataframe['Combination_Key'].fillna(dataframe['Country/Region'] + ", Province not Known", inplace=True)

    return dataframe



print("Null Count of Dataframe 1 = \n", Null_Count(df1))
print("Null Count of Dataframe 2 = \n", Null_Count(df2))

df1 = Province_fill(df1)
df2 = Province_fill(df2)

df1 = Combination_fill(df1)


########################################################################################################################

print("new dataframe = \n", df1.head(), "new dataframe = \n", df2.head())

########################################################################################################################

df1 = df1.rename(columns={'Country/Region': 'country'})
df1 = df1.rename(columns={'iso3' : 'isocode'})

# df1.to_json("who_global_confirmed_cases.json", orient='records')
df1.to_csv("A:\College\DAP-Project\Cases_and_Death_Rates\Data\who_global_confirmed_Cases.csv")
# df2.to_csv("who_global_deaths.csv")
# df3.to_csv("who_US_Deaths.csv")
# df4.to_csv("who_US_Confirmed_Cases.csv")
