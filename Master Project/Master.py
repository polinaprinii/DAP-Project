"""
    Creating final python file which is a compilation of all coding files written by all team members.
    The file is a combination of the following sub-folders from the Master Project folder.
    - Vaccine_Analysis_by_Country
    - Cases_and_Death_Rates
    - Restriction_and_Testing_Analysis

    There is no right or wrong order of importing the files as long as the above sub-folders and their contents prior
    to calling the "Linear Regression Final Dataset" folder, specifically the Final_Dataset.ipynb file.
    The above file performs the merging off all three individual exports for a final master csv file for the linear
    regression.
"""

"""
    Importing the python files from Vaccine_Analysis_by_Country
"""
# Extracting raw data from GitHub. Please change file path for code to successfully run.
import Vaccine_Analysis_by_Country.Main_Project.Extract_Raw_Data

"""
Pushing raw data into MongoDB for pre-processing stage.
Please change file path for code to successfully run.
Please provide MongoDB credentials.
"""
import Vaccine_Analysis_by_Country.Main_Project.MongoDB_Import

"""
Transforming data in MongoDB in preparation to push to PostgreSQL for storage.
Please change file path for code to successfully run.
Please provide MongoDB credentials and IP address.
"""
import Vaccine_Analysis_by_Country.Main_Project.MongoDb_Transformations

"""
Importing data into PostgreSQL and assigning relationships.
Please change file path for code to successfully run.
Please provide MongoDB credentials and IP address.
Please provide PostgreSQL credentials and IP address.
"""
import Vaccine_Analysis_by_Country.Main_Project.PostgreSQL_ImportTransform

"""
Exporting final CSV for regression analysis and data visualisation.
Please change file path for code to successfully run.
Please provide PostgreSQL credentials and IP address.
"""

import Vaccine_Analysis_by_Country.Main_Project.PostgreSQLExport

# Drafting supporting data visualisations for the understanding of the data. Please change file path for code to successfully run.
import Vaccine_Analysis_by_Country.Main_Project.Data_Visualisation


"""
    Importing the python files from Cases_and_Death_Rates
"""
# Scrapping data from Github and saving it locally. Please change file path for code to successfully run.
import Cases_and_Death_Rates.Scripts.GitHub_Data_Request

"""
Writing raw datasets to MongoDB.
Please change file path for code to successfully run.
Please provide MongoDB credentials and IP address.

"""
import Cases_and_Death_Rates.Scripts.Read_Dataset_Write_To_Database

"""
Read from MongoDB, transform data and write to MongoDB.
Please provide MongoDB credentials and IP address.
"""
import Cases_and_Death_Rates.Scripts.Dataset_Transformation

"""
Exploratory data analysis of Covid data.
Please provide MongoDB credentials and IP address.
"""
import Cases_and_Death_Rates.Scripts.EDA_Of_Covid_Data

"""
Visualisation of transformed data.
Please provide MongoDB credentials and IP address.
"""
import Cases_and_Death_Rates.Scripts.Data_Visualisation

"""
Scrapping data from Github, transforming and writing to PostgreSQL and local.
Please provide PostgreSQL credentials and IP address.
Please change file path for code to successfully run.
"""
import Cases_and_Death_Rates.Scripts.ETL_For_MLR

"""
Restriction_and_Testing_Analysis code work was undertaken using the R scripting language.
Having researched the topic to to call .r files into this Master.py file, it appeared inadvisable to perform such 
actions as Python and R are two different languages. 

Thus please run the "Restriction_and_Testing_Analysis" folder and it's respective script files outside of this python
file.
Please note that there may be a requirement to change file paths as well as provide credentials and ip information.
"""