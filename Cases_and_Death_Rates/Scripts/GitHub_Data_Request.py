import io
import pandas as pd
import pycountry
import requests.exceptions
import country_converter as coco

pd.options.mode.chained_assignment = None


# This script will download all RAW CSV files from
# https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
#I will then Save Them Locally
# Assigning the correct RAW github Urls to Variables

url1 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/" \
       "csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url2 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/" \
       "csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url3 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/" \
       "csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
url4 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/" \
       "csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
all_urls = [url1, url2, url3, url4]
# Reading the content of the URL



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
    # Checking that the dataframes are not empty, printing success notice.
    if df1.size and df2.size and df3.size and df4.size > 0:
        print("data successfully imported and stored in dataframe.")

# Printing the first 5 rows of each dataframe.

finally:
    all_dfs = [df1, df2, df3, df4]
    for i in all_dfs:
        print(i.head(5))

# Saving the CSV files locally

df1.to_csv(
    r'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\RAW_who_global_confirmed_Cases.csv')
df2.to_csv(
    r'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\RAW_who_global_deaths.csv')
df3.to_csv(
    r'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\RAW_who_US_Deaths.csv')
df4.to_csv(
    r'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\RAW_who_US_Confirmed_Cases.csv')

