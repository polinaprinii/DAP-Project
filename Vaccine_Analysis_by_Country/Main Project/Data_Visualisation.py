# Importing needed packages to visualise our data.

import pandas as pd
import plotly.express as px


# Reading csv file.
df = pd.read_csv("/Users/polinaprinii/Documents/GitHub/DAP-Project/Vaccine_Analysis_by_Country/Main Project/CSV Files/finalexport.csv")

# Checking if read was successful.
print(df.head())

# Split the data into smaller sub dataframes to
lowsub = df[df["totalvaccinations"] < 10000000]

midsub = df[(df["totalvaccinations"] > 10000000) & (df["totalvaccinations"] < 100000000)]

highsub = df[df["totalvaccinations"] > 100000000]


# Plot horizontal bar chart
plot = px.data.tips()
fig = px.bar(lowsub, x="totalvaccinations", y="country", title="Total Vaccinations Administered by Country",
             color="fullyvacnumber", text="totalvaccinations", labels=dict(totalvaccinations="Total Vaccinations (2 dose)", country="Country",
                                                 fullyvacnumber="Number of Fully Vaccinated", ), orientation='h')
fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
fig.update_xaxes(type="log")
#fig.update_layout(yaxis = dict(tickfont = dict(size=7)))
fig.update_traces(width=5, textposition='inside', textfont_size=14)
fig.show()

# TODO: Increase font of the text feature in the bar chart as well as group other sub dataframes into the bar chart.


# Attempting to built a Choropleth Map:

import plotly.express as px

worldMap = px.choropleth(lowsub,
                title="World Map of Fully Vaccinated",
                locations ="isocode",
                color="fullyvacnumber",
                hover_name="country", # column to add to hover information
                color_continuous_scale=px.colors.sequential.Viridis,)
worldMap.update_layout(
    coloraxis_colorbar=dict(
        title="Number of Fully Vaccinated"))
worldMap.show()

# TODO: Group all three sub datasets into one aka, 3 pages of same graph.