# Importing necessary packages to allows us to push JSON files into MongoDB

import json                             # JSON package as we are importing JSON files into MongoDB

import pymongo.errors
from pymongo import MongoClient         # Pymongo package which provides tools for working with MongoDB
                                        # MongoClient tool to connect to a MongoDB

# Setting up our connection:
try:
    my_DB = MongoClient('mongodb://192.168.56.30:27017')
    print('Ping successful: ', my_DB.admin.command('ping'))

except pymongo.errors.ServerSelectionTimeoutError as Error1:
    print('Oh no, there seems to be an issue in connecting, see bellow:', '\n', Error1)

except Exception as Error2:
    print('Oh no, there seems to be an issue in connecting, see bellow:', '\n', Error2)

# Declaring our database which will hold our collections aka tables.
db = my_DB['Vaccinations_DB']

# Creating our collections aka tables for each JSON file
Collection1 = db['df_1']
Collection2 = db['df_2']
Collection3 = db['df_3']

# Loading the JSON files into the declared collections.
# Loading df_1
with open('D:\Git\DAP-Project\Vaccine_Analysis_by_Country\Main Project\JSON Files\df_1.json') as file1:
    file1_data = json.load(file1)

#Loading df_2
with open('D:\Git\DAP-Project\Vaccine_Analysis_by_Country\Main Project\JSON Files\df_2.json') as file2:
    file2_data = json.load(file2)

# Loading df_3
with open('D:\Git\DAP-Project\Vaccine_Analysis_by_Country\Main Project\JSON Files\df_3.json') as file3:
    file3_data = json.load(file3)

if isinstance(file1_data, list):
    Collection1.insert_many(file1_data)
else:
    Collection1.insert_one(file1_data)

if isinstance(file2_data, list):
    Collection2.insert_many(file2_data)
else:
    Collection2.insert_one(file2_data)

if isinstance(file3_data, list):
    Collection3.insert_many(file3_data)
else:
    Collection3.insert_one(file3_data)

