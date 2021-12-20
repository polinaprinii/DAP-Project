import pandas as pd
import io
import requests
import pycountry
import country_converter as coco
import psycopg2

url_Global_Totals_to_Date = \
    r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master' \
    r'/csse_covid_19_data/csse_covid_19_daily_reports/12-05-2021.csv'
url_US_Totals_to_Date = \
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master' \
    '/csse_covid_19_data/csse_covid_19_daily_reports_us/12-05-2021.csv'

download1 = requests.get(url_Global_Totals_to_Date).content
download2 = requests.get(url_US_Totals_to_Date).content

df1 = pd.read_csv(io.StringIO(download1.decode('utf-8')))
df2 = pd.read_csv(io.StringIO(download2.decode('utf-8')))

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

all_cases_and_deaths["country"].replace({"Korea, South": "South Korea"}, inplace=True)
#
# all_cases_and_deaths.loc[all_cases_and_deaths['country'] == 'US', ['country']] = 'United States'

# noinspection PyTypeChecker
all_cases_and_deaths.to_csv(r'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Data for Multiple Linear '
                            r'Regression\Global_and_US_Confirmed_Cases_And_Deaths.csv')

# Saving the data to a postgresql database on virtual machine

try:
    dbConnection = psycopg2.connect(user="dap",
                                    password="dap",
                                    host="192.168.56.30",
                                    port="5432",
                                    database='postgres'
                                    )
    dbConnection.set_isolation_level(0)  # AUTOCOMMIT

    dbConnection.commit()
    cur = dbConnection.cursor()

    name_Database = "covid_data_for_mlr"

    # Create table statement

    sqlCreateDatabase = "create database " + name_Database + ";"

    # Create a table in PostgreSQL database

    cur.execute(sqlCreateDatabase)

    cur.execute("""
        CREATE TABLE covid_mlr_data(
        index int PRIMARY KEY, 
        iso text ,
        country VARCHAR ,
        confirmed int,
        deaths int
    )
    """)
except (Exception, psycopg2.Error) as dbError:
    print("An error has occured", dbError)
else:
    cur = dbConnection.cursor()
    with open(
            'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Data for Multiple Linear Regression\Global_and_US_Confirmed_Cases_And_Deaths.csv',
            'r') as f:
        # Notice that we don't need the `csv` module.
        next(f)  # Skip the header row.
        cur.copy_from(f, 'covid_mlr_data', sep=',')
finally:
    print("Data successfully written to database")
