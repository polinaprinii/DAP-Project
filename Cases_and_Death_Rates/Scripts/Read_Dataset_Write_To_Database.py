import pandas as pd
import pymongo
import pprint

# this file will read RAW files from local and write them as 4 separate collections to MONGO DB
# Reading RAW files from local storage
try:
    Raw_global_cases = pd.read_csv(
        'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\RAW_who_global_confirmed_Cases.csv')
    Raw_global_deaths = pd.read_csv(
        'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\RAW_who_global_deaths.csv')
    Raw_US_cases = pd.read_csv(
        'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\RAW_who_US_Confirmed_Cases.csv')
    Raw_US_deaths = pd.read_csv(
        'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\RAW_who_US_Deaths.csv')

except FileNotFoundError:
    print("File not found.")
except pd.errors.EmptyDataError:
    print("No data")
except pd.errors.ParserError:
    print("Parse error")
except Exception:
    print("Some other exception")
else:
    print("File Successfully Read")

finally:
    all_dfs = [Raw_global_cases, Raw_global_deaths, Raw_US_deaths, Raw_US_cases]
    for df in all_dfs:
        print(df.head())


# Converting CSV files to Dictionaries
Raw_global_cases = Raw_global_cases.to_dict('records')
Raw_global_deaths = Raw_global_deaths.to_dict('records')
Raw_US_deaths = Raw_US_deaths.to_dict('records')
Raw_US_cases = Raw_US_cases.to_dict('records')


# Connecting to MongoDB
client = pymongo.MongoClient('192.168.56.30', 27017)
# New Mongo Database for the raw data storage
db = client.covid_data

# Creating new collections for the 4 raw files
covid_cases_global = db.covid_cases_global
covid_cases_US = db.covid_cases_US
covid_deaths_global = db.covid_deaths_global
covid_deaths_US = db.covid_deaths_US

# Sending raw files to Collections
Cases_Glob = covid_cases_global.insert_many(Raw_global_cases)
Cases_US = covid_cases_US.insert_many(Raw_US_cases)
Deaths_Glob = covid_deaths_global.insert_many(Raw_global_deaths)
Deaths_US = covid_deaths_US.insert_many(Raw_US_deaths)



df1 = pd.DataFrame(list(covid_cases_global.find()))
df2 = pd.DataFrame(list(covid_cases_US.find()))
df3 = pd.DataFrame(list(covid_deaths_global.find()))
df4 = pd.DataFrame(list(covid_deaths_US.find()))


#df1.to_csv(r'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\TEST_FROM_MONGODB.csv')

