# Importing necessary packages to allow to transform data in MongoDB.
import pymongo.errors
from pymongo import MongoClient
from MongoDB_Import import db
import psycopg2
import pandas as pd
import pandas.io.sql as sqlio

# Specify connection to MongoDB database.
my_client = MongoClient('mongodb://192.168.56.30:27017')

# Specify DB in use.
my_db = my_client['Vaccinations_DB']

# Array for Countries collection.
country = []
iso = []

# For loop to populate.
countryData = db.Countries.find()
for record in countryData:
    country.append(record['Country'])
    iso.append(record['ISO_Code'])

# Arrays to hold MongoDB data - Holds Total_Vaccinations_Worldwide collection data.
countryVac = []
isoVac = []
totalVac = []
totalBoost = []
numberFullyVac = []

# For loop to populate said arrays, pulls from Total_Vaccinations_Worldwide collection.
data = db.Total_Vaccinations_Worldwide.find()
for record in data:
    countryVac.append(record['Country'])
    isoVac.append(record['ISO_Code'])
    totalVac.append(record['Total_Vaccinations_Administered'])
    totalBoost.append(record['Total_Boosters_Administered'])
    numberFullyVac.append(record['Number_of_People_Fully_Vaccinated'])

# Creating tables in PostgreSQl:
createCountries = """
CREATE TABLE Countries(
ISOCode varchar(50) PRIMARY KEY,
Country varchar(100)
) ;
"""

createTotalVacs = """
CREATE TABLE TotalVaccinationsWorldwide(
Country varchar(100) PRIMARY KEY,
ISOCode varchar(50), 
TotalVaccinations numeric(12,1),
TotalBooster numeric (12,1),
FullyVaccinated numeric (12,1),
FOREIGN KEY (ISOCode) REFERENCES Countries(ISOCode)
);
"""

# Connection to PostgreSQl
try:
    dbConnection = psycopg2.connect(user = "dap",
                                   password = "dap",
                                   host = "192.168.56.30",
                                   port = "5432",
                                   database = "postgres")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    # TODO: Add if to not run this if the tables exist.
    #dbCursor.execute(createCountries)
    #dbCursor.execute(createTotalVacs)
    dbCursor.close()

except (Exception , psycopg2.Error) as dbError :
    print("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection):
        dbConnection.close()



# Populating tables, sending rows to Countries table:
s = ""
s += "INSERT INTO Countries "
s += "("
s += "ISOCode"
s += ", Country"
s += ")"
s += " VALUES"
s += "("
for i, c in zip(iso, country):
    s += "'" + i + "'"
    s += "," + c
s += ")"

try:
    dbConnection = psycopg2.connect(user = "dap",
                                   password = "dap",
                                   host = "192.168.56.30",
                                   port = "5432",
                                   database = "postgres")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    dbCursor.execute(s)
    dbCursor.close()

except (Exception , psycopg2.Error) as dbError :
    print("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection):
        dbConnection.close()