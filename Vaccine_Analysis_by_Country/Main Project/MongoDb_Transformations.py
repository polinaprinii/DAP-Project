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
    print('One no an error: ', pyerror)

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
print(my_db.list_collection_names())

