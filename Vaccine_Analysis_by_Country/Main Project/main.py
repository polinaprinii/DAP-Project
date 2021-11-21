# Importing the pandas package to work with csv files and later convert them to JSON.

import pandas as pd

pd. set_option('display.max_rows', 500)

# Next we move to creating variables which will hold our three dataset.
# Using the read_csv() function we can directly specify a path to the csv file in the git repository using the "raw" view.

# Calling our first dataset "vaccinatios.csv"

df_1 = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv')
print(df_1)