import pandas as pd
import io
import requests
import pycountry
import country_converter as coco

url_Global_Totals_to_Date = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/12-05-2021.csv'
url_US_Totals_to_Date = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/12-05-2021.csv'

download1 = requests.get(url_Global_Totals_to_Date).content
download2 = requests.get(url_US_Totals_to_Date).content

df1 = pd.read_csv(io.StringIO(download1.decode('utf-8')))
df2 = pd.read_csv(io.StringIO(download2.decode('utf-8')))

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


###########this will be a new file which will start with pulling the dataset from above FROM Postgres####################


print(df1.columns)
print(df2.columns)

df1.drop(['FIPS', 'Admin2', 'Province_State', 'Last_Update',
          'Lat', 'Long_', 'Recovered', 'Active',
          'Combined_Key', 'Incident_Rate',
          'Case_Fatality_Ratio'], axis=1, inplace=True)

df2.drop(['Province_State', 'Last_Update', 'Lat', 'Long_',
          'Recovered', 'Active', 'FIPS', 'Incident_Rate',
          'Total_Test_Results', 'People_Hospitalized',
          'Case_Fatality_Ratio', 'UID', 'Testing_Rate',
          'Hospitalization_Rate'], axis=1, inplace=True)


df1['isocode'] = df1.groupby('Country_Region')['Country_Region'].transform(coco.convert)

cols1 = df1.columns.tolist()
cols1 = cols1[-1:] + cols1[:-1]
df1 = df1[cols1]

cols1 = df2.columns.tolist()
cols1 = cols1[-1:] + cols1[:-1]
df2 = df2[cols1]

df1 = df1.rename(columns={'Country_Region': 'country'})
df2 = df2.rename(columns={'Country_Region': 'country'})
df2 = df2.rename(columns={'ISO3': 'isocode'})

df1.drop(df1[df1.isocode == 'nan'].index, inplace=True)

df1.drop(df1[df1.country == 'US'].index, inplace=True)

dataframes_to_concat = [df1, df2]

all_cases_and_deaths = pd.concat(dataframes_to_concat, ignore_index=True)

all_cases_and_deaths = all_cases_and_deaths.groupby(['isocode', 'country']).sum().reset_index()

all_cases_and_deaths.groupby(['country'])

#
# all_cases_and_deaths.loc[all_cases_and_deaths['country'] == 'US', ['country']] = 'United States'

# noinspection PyTypeChecker
all_cases_and_deaths.to_csv(r'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Data for Multiple Linear '
                            r'Regression\Global_and_US_Confirmed_Cases_And_Deaths.csv')
