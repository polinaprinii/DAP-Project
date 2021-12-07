import io

import kaggle
import pandas as pd
import requests

try:
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    api.dataset_download_file('antgoldbloom/covid19-data-from-john-hopkins-university',
                              file_name='CONVENIENT_global_confirmed_cases.csv')
except:
    print('An error has occurred, please check information provided and try again.')

else:
    print("Connection Made")

finally:
    print('Your File is now ready, Enjoy!')

# download = 'CONVENIENT_global_confirmed_cases.csv'
df = pd.read_csv('CONVENIENT_global_confirmed_cases.csv')

print(df.head())