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
numberFullyVac = []

# For loop to populate above arrays, pulls from Total_Vaccinations_Worldwide collection.
data = db.Total_Vaccinations_Worldwide.find()
for record in data:
    countryVac.append(record['Country'])
    isoVac.append(record['ISO_Code'])
    totalVac.append(record['Total_Vaccinations_Administered'])
    totalBoost.append(record['Total_Boosters_Administered'])
    numberFullyVac.append(record['Number_of_People_Fully_Vaccinated'])

# Creating tables in PostgreSQl (Countries & TotalVaccinationsWorldwide) if they dont exist:
createCountries = """
CREATE TABLE IF NOT EXISTS Countries(
ISOCode varchar(50) PRIMARY KEY,
Country varchar(100)
) ;
"""

createTotalVacs = """
CREATE TABLE IF NOT EXISTS TotalVaccinationsWorldwide (
Country varchar(100) PRIMARY KEY,
ISOCode varchar(50), 
TotalVaccinations numeric(12,1),
TotalBooster numeric (12,1),
FullyVaccinated numeric (12,1),
FOREIGN KEY (ISOCode) REFERENCES Countries(ISOCode)
);
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

    dbCursor.execute(createCountries)
    dbCursor.execute(createTotalVacs)

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

# Populating above lists in prep to populate tables later on.
# Countries table:
for index, i in enumerate(country):
    s = ""
    """Regex logic to find and replace an instance of a single quote with double single quotes.
    Performed due to PostgreSQL not being able to read ' whilst data is in a string. '' required to resolve issue. 
    
    On conflict with the same value do not insert the row, avoids errors from postgres on duplicates.
    """
    s += "INSERT INTO Countries(ISOCode, Country) VALUES('" + iso[index] + "' , '" + re.sub("'", "''", country[index]) + "') ON CONFLICT (IsoCode) DO NOTHING"
    insertCountryList.append(s)

# TotalVaccinationsWorldwide:
for index, i in enumerate(countryVac):
    s = ""
    """Additional Regex logic added to replace Null with 0 as TotalVaccinations, TotalBooster, FullyVaccinated 
    columns are numeric type. 
    
    On conflict with the same value do not insert the row, avoids errors from postgres on duplicates.
    """
    s += "INSERT INTO TotalVaccinationsWorldwide(Country, ISOCode, TotalVaccinations, TotalBooster, FullyVaccinated  ) " \
        "VALUES('" \
         + re.sub("'", "''", countryVac[index]) + "' , '" \
         + isoVac[index] + "' , '" \
         + re.sub("None", "0", str(totalVac[index])) + "' , '" \
         + re.sub("None", "0", str(totalBoost[index])) + "' , '" \
         + re.sub("None", "0", str(numberFullyVac[index])) + "') " \
         + "ON CONFLICT (Country) DO UPDATE SET TotalVaccinations = '" + re.sub("None", "0", str(totalVac[index])) \
         + "', TotalBooster ='" + re.sub("None", "0", str(totalBoost[index])) \
         + "', FullyVaccinated ='" + re.sub("None", "0", str(numberFullyVac[index])) + "'"
    insertVaccinationsList.append(s)

# Populating tables, sending rows to both tables:
try:
    dbConnection = psycopg2.connect(user="dap",
                                    password="dap",
                                    host="192.168.56.30",
                                    port="5432",
                                    database="postgres")
    dbConnection.set_isolation_level(0)  # AUTOCOMMIT
    dbCursor = dbConnection.cursor()

    # Countries table:
    for i in insertCountryList:
        dbCursor.execute(i)

    # TotalVaccinationsWorldwide:
    for j in insertVaccinationsList:
        dbCursor.execute(j)

    dbCursor.close()

except (Exception, psycopg2.Error) as dbError:
    print("Error while connecting to PostgreSQL", dbError)

finally:
    if (dbConnection):
        dbConnection.close()

