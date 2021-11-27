# Importing the necessary URL errors for us to except a no internet connection situation.
from urllib.error import URLError

# Importing the pandas package to work with csv files and later convert them to JSON.
import pandas as pd

# Importing OS for interacting with the operating system.
import os

# Next we move to creating variables which will hold our three dataset.
# Using the read_csv() function we can directly specify a path to the csv file in the git repository using the "raw" view.

# Specify variaable to hold our raw URL from Git.
vac_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'  # Vaccinations dataset.
man_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations-by-manufacturer.csv'  # Vaccinations by manufacturer dataset.
age_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations-by-age-group.csv'  # Vaccinations by age groups dataset.

# Calling our first dataset "vaccinations.csv"
# Adding exception handling to cover cases such as wrong url specified, no internet/network is down, as well as adding an if clasue in the case the git repository gets shut down.

dataPopulated = False  # A variable to check if we will be pulling from the web or locally, intially set to false as web is the desired outcome.

#df_1 ... df_3 read csv files from git.
try:
    df_1 = pd.read_csv(vac_url)
    df_2 = pd.read_csv(man_url)
    df_3 = pd.read_csv(age_url)
    if df_1.size and df_2.size and df_3.size > 0:  # Checking if our dataframes are not empty
        dataPopulated = True  # Setting the variable to true which completes our code as successful.
        print('Getting data from Git repo successful', '\n')
        print('Vaccinations data columns are:', '\n', df_1.columns.values, '\n', '\n',
              'Vaccinations by manufacturers data columns are:', '\n', df_2.columns.values, '\n', '\n',
              'Vaccinations by age data columns are:', '\n', df_3.columns.values,
              '\n')  # prints the columns names for all 3 datasets
        print('Vaccinations data contains:', len(df_1), 'rows.', '\n', '\n',
              'Vaccinations by manufacturer data contains:', len(df_2), 'rows.', '\n', '\n',
              'Vaccinations by age data contains:', len(df_3), 'rows.', '\n')  # count rows in all 3 data frames

# The above prints & at the same time confirms that the read was successful.

except URLError:
    print('Oh uh! seems your network is down')
    print('Please check you internet connection \n')

except Exception as error1:
    print('There seems to be an error:', error1)

if not dataPopulated:  # Code jumps to pulling the file from local in the case theres no internet connection.
    df_1 = pd.read_csv(r'C:\Users\Rober\Documents\Datasets\vaccinations.csv')
    df_2 = pd.read_csv(r'C:\Users\Rober\Documents\Datasets\vaccinations-by-manufacturer.csv')
    df_3 = pd.read_csv(r'C:\Users\Rober\Documents\Datasets\vaccinations-by-age-group.csv')
    print('Getting data from Local Machine as there is no Internet connection', '\n')
    print('Vaccinations data columns are:', '\n', df_1.columns.values, '\n', '\n',
          'Vaccinations by manufacturers data columns are:', '\n', df_2.columns.values, '\n', '\n',
          'Vaccinations by age data columns are:', '\n', df_3.columns.values,
          '\n')  # prints the columns names for all 3 datasets
    print('Vaccinations data contains:', len(df_1), 'rows.', '\n', '\n', 'Vaccinations by manufacturer data contains:',
          len(df_2), 'rows.', '\n', '\n', 'Vaccinations by age data contains:', len(df_3), 'rows.',
          '\n')  # count rows in all 3 data frames


# Create function to convert from CSV to JSON, function applies to all 3 CSV datasets.
def convertCsvToJson(file1, file2, file3):
    # Storing the 3 file-paths in variables.
    filePath_1 = 'D:\Git\DAP-Project\Vaccine_Analysis_by_Country\Main Project\JSON Files\df_1.json'
    filePath_2 = 'D:\Git\DAP-Project\Vaccine_Analysis_by_Country\Main Project\JSON Files\df_2.json'
    filePath_3 = 'D:\Git\DAP-Project\Vaccine_Analysis_by_Country\Main Project\JSON Files\df_3.json'


    filePaths = [filePath_1, filePath_2, filePath_3]    # List of paths to all JSON  files.
    files = [file1, file2, file3]                       # List of csv files.

    try:
        """
        Loop through filePaths and enumerate them to give them an index. Enumerate gives index top items in list.
        Check if every file paths exists, True = remove file, else prints message and creates file.
        Create file by using the index of filePaths item to write to file. 
        """

        for index, filePath in enumerate(filePaths):
            if os.path.exists(filePath):
                os.remove(filePath)
            else:
                print('File', filePath, 'does not exist, creating it.')

            with open(filePath, 'w') as f:
                f.write(files[index].to_json(orient='records', indent=2))

    except OSError as error2:
        print('Oh no there seems to be an error with the files, see below:', '\n',
              error2)

    except Exception as error3:
        print('There seems to be an error when converting from CSV to JSON, please see below:', '\n',
              error3)

# Executing the function.
convertCsvToJson(df_1, df_2, df_3)
