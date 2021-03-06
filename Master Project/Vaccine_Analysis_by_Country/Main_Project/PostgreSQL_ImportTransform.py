# Importing necessary packages to allow to import and transform data into PostgreSQL.
import pymongo.errors
from pymongo import MongoClient
from MongoDB_Import import db
import psycopg2
import re

# Specify connection to MongoDB database.
my_client = MongoClient('mongodb://192.168.56.30:27017')

# Arrays for to hold MongoDB data - holds Countries collection.
country = []
iso = []

# For loop to populate above arrays, pulls from Countries collection.
countryData = db.Countries.find()
for record in countryData:
    country.append(record['Country'])
    iso.append(record['ISO_Code'])

# Arrays to hold MongoDB data - holds Total_Vaccinations_Worldwide collection data.
countryVac = []
isoVac = []
totalVac = []
totalBoost = []

# For loop to populate above arrays, pulls from Total_Vaccinations_Worldwide collection.
data = db.Total_Vaccinations_Worldwide.find()
for record in data:
    countryVac.append(record['Country'])
    isoVac.append(record['ISO_Code'])
    totalVac.append(record['Total_Vaccinations_Administered'])
    totalBoost.append(record['Total_Boosters_Administered'])

# Arrays for to hold MongoDB data - holds People_Fully_Vaccinated collection.
countryPeople = []
isoPeople = []
numberFullyVac = []

# For loop to populate above arrays, pulls from People_Fully_Vaccinated collection.
data2 = db.People_Fully_Vaccinated.find()
for record in data2:
    countryPeople.append(record['Country'])
    isoPeople.append(record['ISO_Code'])
    numberFullyVac.append(record['Number_of_People_Fully_Vaccinated'])

# Creating tables in PostgreSQl (Countries & TotalVaccinationsWorldwide):
createCountries = """
CREATE TABLE country(
ISOCode varchar(50) PRIMARY KEY,
Country varchar(100) 
) ;
"""

createTotalVacs = """
CREATE TABLE totalvac(
Country varchar(100) PRIMARY KEY,
ISOCode varchar(50), 
TotalVaccinations numeric(12,1),
TotalBooster numeric (12,1),
FOREIGN KEY (ISOCode) REFERENCES Countries(ISOCode)
);
"""

createPeopleVacs = """
CREATE TABLE vaccinations(
Country varchar(100) PRIMARY KEY,
ISOCode varchar(50), 
FullyVacNumber numeric (12,1),
FOREIGN KEY (ISOCode) REFERENCES Countries(ISOCode)
);
"""

# Variables to hold SQL syntax to check if tables exist to avoid table exists errors.
countryTableExists = """
SELECT COUNT(*) FROM country
"""

totalVacTableExists = """
SELECT COUNT(*) FROM totalvac
"""

totalPeopleVacTableExists = """
SELECT COUNT(*) FROM vaccinations
"""

# Connection to PostgreSQl Server on VM.
try:
    # PostgreSQl credentials.
    dbConnection = psycopg2.connect(user="dap",
                                    password="dap",
                                    host="192.168.56.30",
                                    port="5432",
                                    database="postgres")
    dbConnection.set_isolation_level(0)  # AUTOCOMMIT
    dbCursor = dbConnection.cursor()

    # Checking if table exist to not create twice for both Countries and TotalVaccinationsWorldwide.
    dbCursor.execute(countryTableExists)
    countryCount = dbCursor.fetchall()
    if not countryCount[0][0] > 0:
        dbCursor.execute(createCountries)

    dbCursor.execute(totalVacTableExists)
    totalVacCount = dbCursor.fetchall()
    if not totalVacCount[0][0] > 0:
        dbCursor.execute(createTotalVacs)

    # dbCursor.execute(totalPeopleVacTableExists)
    totalPeopleCount = dbCursor.fetchall()
    if not totalPeopleCount[0][0] > 0:
        dbCursor.execute(createPeopleVacs)

    dbCursor.close()

except (Exception, psycopg2.Error) as dbError:
    print("Error while connecting to PostgreSQL", dbError)

finally:
    if (dbConnection):
        dbConnection.close()

# List to hold the Insert Values for populating Countries table in PostgreSQL.
insertCountryList = []

# List to hold the Insert Values for populating TotalVaccinationsWorldwide table in PostgreSQL.
insertVaccinationsList = []

# List to hold the Insert Values for populating PeopleFullyVaccinated table in PostgreSQL.
insertPeopleList = []

# Populating above lists in prep to populate tables later on.
# Countries table:
for index, i in enumerate(country):
    s = ""
    """Regex logic to find and replace an instance of a single quote with double single quotes.
    Performed due to PostgreSQL not being able to read ' whilst data is in a string. '' required to resolve issue. 
    """
    s += "INSERT INTO country(ISOCode, Country) VALUES('" + iso[index] + "' , '" \
         + re.sub("'", "''", country[index]) + "') ON CONFLICT DO NOTHING"
    insertCountryList.append(s)

# TotalVaccinationsWorldwide:
for index, i in enumerate(countryVac):
    s = ""
    """Additional Regex logic added to replace Null with 0 as TotalVaccinations, TotalBooster, FullyVaccinated 
    columns are numeric type. 
    """
    s += "INSERT INTO totalvac(Country, ISOCode, TotalVaccinations, TotalBooster  ) VALUES('" + re.sub(
        "'", "''", countryVac[index]) + "' , '" + isoVac[index] + "' , '" + re.sub("None", "0", str(totalVac[index]))\
         + "' , '" + re.sub("None", "0", str(totalBoost[index])) + "') ON CONFLICT DO NOTHING"
    insertVaccinationsList.append(s)

#  PeopleFullyVaccinated:
for index, i in enumerate(countryPeople):
    s = ""
    """Regex logic to find and replace an instance of a single quote with double single quotes.
    Performed due to PostgreSQL not being able to read ' whilst data is in a string. '' required to resolve issue. 
    """
    s += "INSERT INTO vaccinations(Country, ISOCode, FullyVacNumber) VALUES('" + re.sub(
        "'", "''", countryPeople[index]) + "' , '" + isoPeople[index] + "' , '" + re.sub("None", "0", str(numberFullyVac[index])) + "') ON CONFLICT DO NOTHING"
    insertPeopleList.append(s)


# Populating tables, sending rows to both tables:
try:
    dbConnection = psycopg2.connect(user="dap",
                                    password="dap",
                                    host="192.168.56.30",
                                    port="5432",
                                    database="postgres")
    dbConnection.set_isolation_level(0)  # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    
    # TODO: Identify the correct method in PostgreSQL to either delete from or truncate table to avoid duplicate error.

    # Countries table:
    for i in insertCountryList:
        dbCursor.execute(i)

    # TotalVaccinationsWorldwide:
    for j in insertVaccinationsList:
        dbCursor.execute(j)

    # TotalVaccinationsWorldwide:
    for y in insertPeopleList:
        dbCursor.execute(y)

    dbCursor.close()

except (Exception, psycopg2.Error) as dbError:
    print("Error while connecting to PostgreSQL", dbError)

finally:
    if (dbConnection):
        dbConnection.close()

