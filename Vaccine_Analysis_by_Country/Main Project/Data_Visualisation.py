# Importing needed packages to visualise our data.

import pandas as pd
import plotly.express as px

# Reading csv file.
df = pd.read_csv("D:/Git/DAP-Project/Vaccine_Analysis_by_Country/Main Project/CSV Files/finalexport.csv")

# Checking if read was successful.
print(df.head())

# Plot horizontalbar chart
plot = px.data.tips()
fig = px.bar(df, x="totalvaccinations", y="country", title="Total Vaccinations by Country", color="totalvaccinations", orientation='h')
fig.update_layout(yaxis={'categoryorder':'category descending'})
fig.update_xaxes(type="log")
#fig.update_xaxes(tick0=1000000, dtick=1500000)
fig.show()

# TODO: Figure out why not all country display on the y axis and make easier to read.