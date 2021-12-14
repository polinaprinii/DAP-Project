# Importing needed packages to visualise our data.

import pandas as pd
import plotly.express as px


# Reading csv file.
df = pd.read_csv("/Users/polinaprinii/Documents/GitHub/DAP-Project/Vaccine_Analysis_by_Country/Main Project/CSV Files/finalexport.csv")

# Checking if read was successful.
print(df.head())

# # Plot horizontal bar chart
# plot = px.data.tips()
# fig = px.bar(df, x="totalvaccinations", y="country", title="Total Vaccinations Administered by Country",
#              color="fullyvacnumber", labels=dict(totalvaccinations="Total Vaccinations (2 dose)", country="Country",
#                                                  fullyvacnumber="Number of Fully Vaccinated"), orientation='h')
# fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
# fig.update_xaxes(type="log")
# fig.show()

# TODO: Figure out why not all country display on the y axis and make easier to read.


# Attempting to built a Choropleth Map:

import plotly.express as px

df = px.choropleth(df,
                title="World Map of Fully Vaccinated",
                locations ="isocode",
                color="fullyvacnumber",
                hover_name="country", # column to add to hover information
                color_continuous_scale=px.colors.sequential.Viridis,)
df.update_layout(
    coloraxis_colorbar=dict(
        title="Number of Fully Vaccinated"))
df.show()