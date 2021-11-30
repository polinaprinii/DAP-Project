# Importing necessary packages to allow to transform data in MongoDB.
import pymongo.errors
from pymongo import MongoClient
from MongoDB_Import import db

# Specify connection to MongoDB database.
my_client = MongoClient('mongodb://192.168.56.30:27017')

# Specify DB in use.
my_db = my_client['Vaccinations_DB']

# Creating collection which wil hold country name and code.
try:
    # Dropping table to avoid duplicates.
    if db.Countries.count() > 0:
        db.Countries.drop()

    db.create_collection('Countries')

except pymongo.errors.PyMongoError as pyerror:
    print('Oh no an error: ', pyerror)

# Populating the Countries collection.
try:
    # A for loop to populate Countries collection using the data from df_1 collection.
    country_name = db.df_1.aggregate([{"$group": {"_id": {'location': "$location", 'iso_code': "$iso_code"}}}])

    for name in country_name:
        db.Countries.insert_one(
            {
                'Country': name['_id']['location'],
                'ISO_Code': name['_id']['iso_code']
            }
        )

except pymongo.errors.PyMongoError as error:
    print('There was an error populating the Countries table:', error)

# Print a value from collection as validation.
print(list(db.Countries.find({'Country': "Poland"})), '\n')

# Check if collection exists
print(my_db.list_collection_names(), '\n')

# Creating collection which will be a combination of all three datasets (df_1, df_2 and df_3).
try:
    if db.Total_Vaccinations_Worldwide.count() > 0:
        db.Total_Vaccinations_Worldwide.drop()

    db.create_collection('Total_Vaccinations_Worldwide')

except pymongo.errors.PyMongoError as pyerror2:
    print('Oh no an error: ', pyerror2)

# Populating the Total_Vaccinations_Worldwide
try:
    # A for loop to populate Total_Vaccinations_Worldwide collection using the data from df_1 collection.
    total_vac_data = db.df_1.aggregate([
        {"$match": {
            "date": "2021-11-24"
        }},
        {"$group": {
            "_id": "$location",
            "Iso_Code": {"$first": "$iso_code"},
            "Total_Vaccinations_Administered": {"$first": "$total_vaccinations"},
            "Total_Boosters_Administered": {"$first": "$total_boosters"},
            "Number_of_People_Fully_Vaccinated": {"$first": "$people_fully_vaccinated"},
        }}])

    for data in total_vac_data:
        db.Total_Vaccinations_Worldwide.insert_one(
            {
                'Country': data['_id'],
                'ISO_Code': data['Iso_Code'],
                'Total_Vaccinations_Administered': data['Total_Vaccinations_Administered'],
                'Total_Boosters_Administered': data['Total_Boosters_Administered'],
                'Number_of_People_Fully_Vaccinated': data['Number_of_People_Fully_Vaccinated']
            }
        )

except pymongo.errors.PyMongoError as error:
    print('There was an error populating the Countries table:', error)
