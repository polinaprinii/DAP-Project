# Importing the necessary URL errors for us to except a no internet connection situation.
from urllib.error import URLError

# Importing the pandas package to work with csv files and later convert them to JSON.
import pandas as pd

# Next we move to creating variables which will hold our three dataset.
# Using the read_csv() function we can directly specify a path to the csv file in the git repository using the "raw" view.

#Specify variaable to hold our raw URL from Git.
vac_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
man_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations-by-manufacturer.csv'
age_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations-by-age-group.csv'

# Calling our first dataset "vaccinations.csv"
# Adding exception handling to cover cases such as wrong url specified, no internet/network is down, as well as adding an if clasue in the case the git repository gets shut down.

dataPopulated = False # A variable to check if we will be pulling from the web or locally, intially set to false as web is the desired outcome.

try:
    df_1 = pd.read_csv(vac_url)     # reading the raw vaccinations.csv file from git.
    df_2 = pd.read_csv(man_url)     # reading the raw vaccinations.csv file from git.
    df_3 = pd.read_csv(age_url)  # reading the raw vaccinations.csv file from git.
    if df_1.size and df_2.size and df_3.size > 0:   # Checking if our dataframes are not empty
        dataPopulated = True    # Setting the variable to true which completes our code as successful.
        print('Getting data from Git repo successful', '\n')
        print('Vaccinations data columns are:', '\n',  df_1.columns.values, '\n', '\n',
              'Vaccinations by manufacturers data columns are:', '\n', df_2.columns.values, '\n', '\n',
              'Vaccinations by age data columns are:', '\n', df_3.columns.values, '\n')  # prints the columns names for all 3 datasets
        print('Vaccinations data contains:', len(df_1), 'rows.', '\n', '\n',
              'Vaccinations by manufacturer data contains:', len(df_2), 'rows.', '\n', '\n',
              'Vaccinations by age data contains:', len(df_3), 'rows.', '\n')  # count rows in all 3 data frames

# The above prints at the same time confirms that the read was successful.

except URLError:
    print('Oh uh! seems your network is down')
    print('Please check you internet connection \n')

except Exception as error:
    print('There seems to be an error:', error)

if not dataPopulated: # Code jumps to pulling the file from local in the case theres no internet connection.
    df_1 = pd.read_csv(r'C:\Users\Rober\Documents\Datasets\vaccinations.csv')
    df_2 = pd.read_csv(r'C:\Users\Rober\Documents\Datasets\vaccinations-by-manufacturer.csv')  # reading the raw vaccinations.csv file from git.
    df_3 = pd.read_csv(r'C:\Users\Rober\Documents\Datasets\vaccinations-by-age-group.csv')  # reading the raw vaccinations.csv file from git.
    print('Getting data from Local Machine as there is no Internet connection', '\n')
    print('Vaccinations data columns are:', '\n', df_1.columns.values, '\n', '\n',
          'Vaccinations by manufacturers data columns are:', '\n', df_2.columns.values, '\n', '\n',
          'Vaccinations by age data columns are:', '\n', df_3.columns.values,
          '\n')  # prints the columns names for all 3 datasets
    print('Vaccinations data contains:', len(df_1), 'rows.', '\n', '\n', 'Vaccinations by manufacturer data contains:',
          len(df_2), 'rows.', '\n', '\n', 'Vaccinations by age data contains:', len(df_3), 'rows.',
          '\n')  # count rows in all 3 data frames