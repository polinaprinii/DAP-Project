# Importing necessary packages to allows us to push JSON files into MongoDB

import json  # JSON package as we are importing JSON files into MongoDB

import pymongo.errors
from pymongo import MongoClient  # Pymongo package which provides tools for working with MongoDB

MONGODB_IP = 'mongodb://192.168.56.30:27017'

# MongoClient tool to connect to a MongoDB

# Setting up our connection:
try:
    my_DB = MongoClient(MONGODB_IP)
    print('Ping successful: ', my_DB.admin.command('ping'))

except pymongo.errors.ServerSelectionTimeoutError as Error1:
    print('Oh no, there seems to be an issue in connecting, see bellow:', '\n', Error1)

except Exception as Error2:
    print('Oh no, there seems to be an issue in connecting, see bellow:', '\n', Error2)

# Declaring our database which will hold our collections aka tables.
db = my_DB['Vaccinations_DB']

collections = [db['df_1'], db['df_2'], db['df_3']]  # List of collections in MongoDB

# Loading the JSON files into the declared collections.
# Loading df_1
filePath_1 = 'D:\Git\DAP-Project\Vaccine_Analysis_by_Country\Main Project\JSON Files\df_1.json'
filePath_2 = 'D:\Git\DAP-Project\Vaccine_Analysis_by_Country\Main Project\JSON Files\df_2.json'
filePath_3 = 'D:\Git\DAP-Project\Vaccine_Analysis_by_Country\Main Project\JSON Files\df_3.json'

filePaths = [filePath_1, filePath_2, filePath_3]

# A function to ensure we only get one import of the JSON file into our declared collections.
def clear_collections(collections):
    for collection in collections:
        if collection.count() > 0:
            collection.drop()

clear_collections(collections)

# Populates collections in MongoDB
def populate_collections(collections, filePaths):

    try:
        """
        Loop through filePaths and enumerate them to give them an index. Enumerate gives index top items in list.
        Open and load JSOn file.
        Populate collections with JSON file.
        """
        for index, filepath in enumerate(filePaths):
            with open(filepath) as f:
                file_data = json.load(f)

            if isinstance(file_data, list):
                collections[index].insert_many(file_data)
            else:
                collections[index].insert_one(file_data)

    except pymongo.errors.DuplicateKeyError as Error2:
        print('There seems to be an error when inserting the data', Error2)

    except pymongo.errors.WriteError as Error3:
        print('There seems to be an error when writing the data', Error3)

populate_collections(collections, filePaths)
