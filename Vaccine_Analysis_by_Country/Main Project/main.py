# Importing the pandas package to work with csv files and later convert them to JSON.

import pandas as pd

# Next we move to creating variables which will hold our three dataset.
# Using the read_csv() function we can directly specify a path to the csv file in the git repository using the "raw" view.

# Calling our first dataset "vaccinatios.csv"

df_1 = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv')
print(df_1, '\n')  # perform check to see if the above
print(df_1.columns.values)  # we check if