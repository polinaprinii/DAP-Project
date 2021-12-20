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
    # Dropping collection to avoid duplicates.
    if bool(db.Countries.find_one()):
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

# Creating collection which will be a combination of all three datasets (df_1, df_2 and df_3).
try:
    if bool(db.Total_Vaccinations_Worldwide.find_one()):
        db.Total_Vaccinations_Worldwide.drop()

    db.create_collection('Total_Vaccinations_Worldwide')

except pymongo.errors.PyMongoError as pyerror2:
    print('Oh no an error: ', pyerror2)

# Populating the Total_Vaccinations_Worldwide
try:
    # A for loop to populate Total_Vaccinations_Worldwide collection using the data from df_1 collection.
    total_vac_data = db.df_1.aggregate(
    [{
        '$match': {
           '$and': [{"date": {
                    '$lte': '2021-12-05'
                          }},

                {"total_vaccinations": {
                    '$ne': 'null'}}
            ]
        }
    },
    {'$group': {
        "_id": "$location",
        "Iso_Code": {"$last": "$iso_code"},
        "Date_of_Last_Record": {"$last": "$date"},
        "Total_Vaccinations_Administered": {"$last": "$total_vaccinations"},
        "Total_Boosters_Administered": {"$last": "$total_boosters"}
    }}])

    for data in total_vac_data:
        db.Total_Vaccinations_Worldwide.insert_one(
            {
                'Country': data['_id'],
                'ISO_Code': data['Iso_Code'],
                'Date_of_Last_Record': data['Date_of_Last_Record'],
                'Total_Vaccinations_Administered': data['Total_Vaccinations_Administered'],
                'Total_Boosters_Administered': data['Total_Boosters_Administered']
            }
        )
except pymongo.errors.PyMongoError as error:
    print('There was an error populating the Countries table:', error)

# Creating collection which wil hold number of people fully vaccinated per country.
try:
    # Dropping collection to avoid duplicates.
    if bool(db.People_Fully_Vaccinated.find_one()):
        db.People_Fully_Vaccinated.drop()

    db.create_collection('People_Fully_Vaccinated')

except pymongo.errors.PyMongoError as pyerror:
    print('Oh no an error: ', pyerror)

# Populating the People_Fully_Vaccinated
try:
    # A for loop to populate People_Fully_Vaccinated collection using the data from df_1 collection.
    people_fully = db.df_1.aggregate(
    [{
        '$match': {
           '$and': [{"date": {
                    '$lte': '2021-12-05'
                          }},

                {"people_fully_vaccinated": {
                    '$ne': 'null'}}
            ]
        }
    },
    {'$group': {
        "_id": "$location",
        "Iso_Code": {"$last": "$iso_code"},
        "Number_of_People_Fully_Vaccinated": {"$last": "$people_fully_vaccinated"}
    }}])

    for data in people_fully:
        db.People_Fully_Vaccinated.insert_one(
            {
                'Country': data['_id'],
                'ISO_Code': data['Iso_Code'],
                'Number_of_People_Fully_Vaccinated': data['Number_of_People_Fully_Vaccinated']
            }
        )

except pymongo.errors.PyMongoError as error:
    print('There was an error populating the Countries table:', error)


# Check if collection exists
print('Here are our collections:', '\n', my_db.list_collection_names(), '\n')

