# Importing the
from urllib.error import URLError

# Importing the pandas package to work with csv files and later convert them to JSON.
from urllib.request import urlopen

import pandas as pd

# Next we move to creating variables which will hold our three dataset.
# Using the read_csv() function we can directly specify a path to the csv file in the git repository using the "raw" view.

#Specify variaable to hold our raw URL from Git.

vac_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
# dataPopulated = False

# Calling our first dataset "vaccinations.csv"
# Adding exception handling to cover cases such as wrong url specified, no internet/network is down, as well as adding an else clasue in the case the git repository gets shut down.

dataPopulated = False
try:
    df_1 = pd.read_csv(vac_url)
    if df_1.size > 0:
        dataPopulated = True
        print('Getting data from Git repo successful', '\n')
        print(df_1, '\n')  # prints the dataframe as well as confirms the csv file is read correctly
        print(df_1.columns.values, '\n')  # prints the columns names
        print(df_1.head(20))  # prints the first 20 rows

except URLError:
    print('Oh uh! seems your network is down')
    print('Please check you internet connection \n')
    dataPopulated = False

except Exception as error:
    print('There seems to be an error:', error)

if not dataPopulated:
    df_1 = pd.read_csv(r'C:\Users\Rober\Documents\Datasets\vaccinations.csv')
    print('Getting data from Local Machine as there is no Internet connection', '\n')
    print(df_1, '\n')  # prints the dataframe as well as confirms the csv file is read correctly
    print(df_1.columns.values, '\n')  # prints the columns names
    print(df_1.head(20))  # prints the first 20 rows