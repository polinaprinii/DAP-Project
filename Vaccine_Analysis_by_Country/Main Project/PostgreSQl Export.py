# Importing necessary packages to allow to export PostgreSQl results into CSV.

import pandas.io.sql as sqlio
import psycopg2
import os

query = """
SELECT * 
FROM TotalVaccinationsWorldwide
"""

# Connection to PostgreSQl Server on VM.
try:
    # PostgreSQl credentials.
    dbConnection = psycopg2.connect(user="dap",
                                    password="dap",
                                    host="192.168.56.30",
                                    port="5432",
                                    database="postgres")
    # Setting variable to read above SQl query.
    vaccs_df = sqlio.read_sql_query(query, dbConnection)

except (Exception, psycopg2.Error) as dbError:
    print("Error:", dbError)
finally:
    if (dbConnection):
        dbConnection.close()

# Check to see if PostgreSQL table returns values. 
print(vaccs_df)

# Prepping above SQl query for export.
df = vaccs_df

# Setting path for csv file.
filePath = 'D:/Git/DAP-Project/Vaccine_Analysis_by_Country/Main Project/CSV Files/finalexport.csv'

# If statement to drop or remove file if exists to avoid any errors.
if os.path.exists(filePath):
    os.remove(filePath)

# Exporting above SQL query to CSV file. Adding index equal to false to drop the automatic index column pandas adds
# by standard.
df.to_csv(filePath, index=False)
