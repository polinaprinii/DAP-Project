"""
    Creating final python file which is a compilation of all coding files written by all team members.
    The file is a combination of the following sub-folders from the Master Project folder.
    - Vaccine_Analysis_by_Country
    - Restriction_and_Testing_Analysis
    - Cases_and_Death_Rates

    There is no right or wrong e order of importing the files as long as the above sub-folders and their contents prior
    to calling the "Linear Regression Final Dataset" folder, specifically the Final_Dataset.ipynb file.
    The above file performs the merging off all three individual exports for a final master csv file for the linear
    regression.
"""

"""
    Importing the python files from Vaccine_Analysis_by_Country
"""
# Extracting raw data from GitHub.
import Vaccine_Analysis_by_Country.Main_Project.Extract_Raw_Data

# Pushing raw data into MongoDB for pre-processing stage.
import Vaccine_Analysis_by_Country.Main_Project.MongoDB_Import

# Transforming data in MongoDB in preparation to push to PostgreSQL for storage.
import Vaccine_Analysis_by_Country.Main_Project.MongoDb_Transformations

# Importing data into PostgreSQL and assigning relationships.
import Vaccine_Analysis_by_Country.Main_Project.PostgreSQL_ImportTransform

# Exporting final CSV for regression analysis and data visualisation.
import Vaccine_Analysis_by_Country.Main_Project.PostgreSQLExport

# Drafting supporting data visualisations for the understanding of the data.
import Vaccine_Analysis_by_Country.Main_Project.Data_Visualisation