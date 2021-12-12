# Importing needed packages to visualise our data.

import pandas as pd
import plotly.express as px

# Reading csv file.
df = pd.read_csv("D:/Git/DAP-Project/Vaccine_Analysis_by_Country/Main Project/CSV Files/finalexport.csv")

# Checking if read was successful.
print(df.head())

# Plot horizontalbar chart
plot = px.data.tips()
fig = px.bar(df, x="totalvaccinations", y="country", orientation='h')
fig.show()