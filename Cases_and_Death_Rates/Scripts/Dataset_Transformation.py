import io
import pandas as pd
import pycountry
import requests.exceptions
import country_converter as coco
import pymongo
import pymongo.errors

pd.options.mode.chained_assignment = None
# retrieval of Data from MongoDB
try:
    # Connecting to MongoDB
    client = pymongo.MongoClient('192.168.56.30', 27017)

    # Mongo Database where the raw data is stored
    db = client.covid_data

    # Database Collection Names
    covid_cases_global = db.covid_cases_global
    covid_cases_US = db.covid_cases_US
    covid_deaths_global = db.covid_deaths_global
    covid_deaths_US = db.covid_deaths_US

    # Pulling records from Mongodb to dataframes
    df1 = pd.DataFrame(list(covid_cases_global.find()))
    df2 = pd.DataFrame(list(covid_deaths_global.find()))
    df3 = pd.DataFrame(list(covid_deaths_US.find()))
    df4 = pd.DataFrame(list(covid_cases_US.find()))
except pymongo.errors.ConnectionFailure as ConError:
    print("Error while attempting connection to Database")
except pymongo.errors.NetworkTimeout as NetworkTimeoutError:
    print("The Network has Timed out")
else:
    print("Connection Made")
finally:
    print("Data Read Successful")


# This file which will start with pulling the 4 RAW files from MongoDB and then transforming them.
# Finally outputting 2 files, the first will be global confirmed cases, the second will be global deaths.
# It will then write these to two new collections in MONGO DB

# Adding ISO Column and moving it to be the first column

df1['iso3'] = df1.groupby('Country/Region')['Country/Region'].transform(coco.convert)
df2['iso3'] = df2.groupby('Country/Region')['Country/Region'].transform(coco.convert)

cols1 = df1.columns.tolist()
cols1 = cols1[-1:] + cols1[:-1]
df1 = df1[cols1]

cols2 = df2.columns.tolist()
cols2 = cols2[-1:] + cols2[:-1]
df2 = df2[cols2]


# Adding a Column for combined key of country and province

def combined_key_col_add(dataframe):
    dataframe["Combination_Key"] = dataframe['Country/Region'].str.cat(dataframe['Province/State'], sep=", ")

    combined_key_col = dataframe.pop("Combination_Key")

    dataframe.insert(3, "Combination_Key", combined_key_col)

    return dataframe


df1 = combined_key_col_add(df1)
df2 = combined_key_col_add(df2)


# Checking for null values and backfilling province with country data if nothing exists there already

def null_count(dataframe):
    no_nulls = (dataframe.isnull().sum())

    return print(no_nulls)


def province_fill(dataframe):
    dataframe['Province/State'].fillna(dataframe['Country/Region'], inplace=True)

    return dataframe


def combination_fill(dataframe):
    dataframe['Combination_Key'].fillna(dataframe['Country/Region'] + ", Province not Known", inplace=True)

    return dataframe


print("Null Count of Dataframe 1 = \n", null_count(df1))
print("Null Count of Dataframe 2 = \n", null_count(df2))

df1 = province_fill(df1)
df2 = province_fill(df2)

df1 = combination_fill(df1)

# Dropping unnecessary columns

df1.drop(['Lat', 'Long', 'Combination_Key', '_id', 'Unnamed: 0'], axis=1, inplace=True)
df2.drop(['Lat', 'Long', 'Combination_Key', '_id', 'Unnamed: 0'], axis=1, inplace=True)
df3.drop([
    'UID', 'iso2', 'code3', 'FIPS',
    'Admin2', 'Lat', 'Long_',
    'Combined_Key', 'Population',
    '_id', 'Unnamed: 0'],
    axis=1, inplace=True)
df4.drop([
    'UID', 'iso2', 'code3', 'FIPS',
    'Admin2', 'Lat', 'Long_',
    'Combined_Key', '_id', 'Unnamed: 0'],
    axis=1, inplace=True)

# Renaming Columns for Concatenation

df3 = df3.rename(columns={'Country_Region': 'Country/Region'})
df4 = df4.rename(columns={'Country_Region': 'Country/Region'})
df3 = df3.rename(columns={'Province_State': 'Province/State'})
df4 = df4.rename(columns={'Province_State': 'Province/State'})

# Concatenating Global Files

Global_Confirmed_Cases_Files = [df1, df4]
Global_Confirmed_Cases = pd.concat(Global_Confirmed_Cases_Files, ignore_index=True)
Global_Confirmed_Deaths_Files = [df2, df3]
Global_Confirmed_Deaths = pd.concat(Global_Confirmed_Deaths_Files, ignore_index=True)

# Removing Total US Country Row to avoid redundancy

Global_Confirmed_Deaths.drop([255], axis=0, inplace=True)
Global_Confirmed_Cases.drop([255], axis=0, inplace=True)

# Writing Dataframes to CSV files
# noinspection PyTypeChecker
Global_Confirmed_Cases.to_csv(r"A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for "
                              r"EDA\Global_Confirmed_Cases.csv")
# noinspection PyTypeChecker
Global_Confirmed_Deaths.to_csv(r"A:\College\DAP-Project\Cases_and_Death_Rates\Data\RAW Data for "
                               r"EDA\Global_Confirmed_Deaths.csv")
# Writing files to JSON for validation
Global_Confirmed_Cases.to_json(r"A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for "
                               r"EDA\Global_Confirmed_Cases.json", orient='records')

Global_Confirmed_Deaths.to_json(r"A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for "
                                r"EDA\Global_Confirmed_Deaths.json", orient='records')

# Writing Both Files to MongoDB
# Convert Dataframes to dictionaries
Global_Confirmed_Cases = Global_Confirmed_Cases.to_dict('records')
Global_Confirmed_Deaths = Global_Confirmed_Deaths.to_dict('records')

# Creating new collections for the 4 raw files
covid_cases_clean = db.covid_cases_clean
covid_deaths_clean = db.covid_deaths_clean

try:
    # Sending cleaned files to Collections
    Cases_Clean = covid_cases_clean.insert_many(Global_Confirmed_Cases)
    Deaths_Clean = covid_deaths_clean.insert_many(Global_Confirmed_Deaths)
except pymongo.errors.CollectionInvalid as invalidColError:
    print("collection invalid")
except pymongo.errors.ConnectionFailure as ConError:
    print("Error while trying to connect to the Database.")
except pymongo.errors.WriteError as writeError:
    print("error while trying to write to Database")
else:
    print("Write to Database successful")
finally:
    print(pd.DataFrame(list(covid_cases_clean.find())).head())

    print(pd.DataFrame(list(covid_deaths_clean.find())).head())
