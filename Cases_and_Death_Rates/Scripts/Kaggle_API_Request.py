import io
import zipfile
import kaggle
import pandas as pd
import requests

########################################################################################################################

try:
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    api.dataset_download_file('antgoldbloom/covid19-data-from-john-hopkins-university',
                              file_name='CONVENIENT_global_confirmed_cases.csv',
                              path='A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA')
    api.dataset_download_file('antgoldbloom/covid19-data-from-john-hopkins-university',
                              file_name='CONVENIENT_global_deaths.csv',
                              path='A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA')
    api.dataset_download_file('antgoldbloom/covid19-data-from-john-hopkins-university',
                              file_name='CONVENIENT_us_confirmed_cases.csv',
                              path='A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA')
    api.dataset_download_file('antgoldbloom/covid19-data-from-john-hopkins-university',
                              file_name='CONVENIENT_us_deaths.csv',
                              path='A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA')

except:
    print('An error has occurred, please check information provided and try again.')

else:
    print("Connection Made")

finally:
    print('Your File is now ready')

########################################################################################################################
with zipfile.ZipFile(
        'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\CONVENIENT_us_confirmed_cases.csv.zip',
        'r') as zipref:
    zipref.extractall(r"A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA")

with zipfile.ZipFile('A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\CONVENIENT_us_deaths.csv.zip',
                     'r') as zipref:
    zipref.extractall(r"A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA")

df1 = pd.read_csv('A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\CONVENIENT_global_confirmed_cases.csv', dtype= 'unicode')
df2 = pd.read_csv('A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\CONVENIENT_global_deaths.csv', dtype= 'unicode')
df3 = pd.read_csv('A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\CONVENIENT_us_confirmed_cases.csv', dtype= 'unicode')
df4 = pd.read_csv('A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\CONVENIENT_us_deaths.csv', dtype= 'unicode')

frames = [df1, df2, df3, df4]
for frame in frames:
    print(frame.head())



########################################################################################################################
