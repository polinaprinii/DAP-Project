# Importing needed packages to visualise our data.
import dcc as dcc
import pandas as pd
import plotly.express as px
import pycountry_convert as pc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Reading csv file.
df = pd.read_csv("/Users/polinaprinii/Documents/GitHub/DAP-Project/Vaccine_Analysis_by_Country/Main Project/CSV Files/finalexport.csv")

# Drop all OWID ISO instances.
index_names = df[ df['isocode'].str.contains("OWID") ].index
df.drop(index_names, inplace = True)

"""Replace country names to follow pycountry country name standards. 
This is due to human error when naming countries pulled from the raw dataset.
"""
df['country'] = df['country'].str.replace('Bonaire Sint Eustatius and Saba','Bonaire, Sint Eustatius and Saba')
df['country'] = df['country'].str.replace('Faeroe Islands','Faroe Islands')
df['country'] = df['country'].str.replace("Cote d'Ivoire","Côte d'Ivoire")
df['country'] = df['country'].str.replace("Saint Helena","Saint Helena, Ascension and Tristan da Cunha")
df['country'] = df['country'].str.replace("Curacao","Curaçao")
df['country'] = df['country'].str.replace("Democratic Republic of Congo","Democratic Republic of the Congo")
df['country'] = df['country'].str.replace("Timor","Timor-Leste")

# Converting country name to country code alpha 2 to allow for the extraction of continent using pycountry.
df['country_code_alpha2'] = df['country'].apply(pc.country_name_to_country_alpha2)

# Exporting dataset.
#df.to_csv("D:/Git/DAP-Project/Vaccine_Analysis_by_Country/Main Project/CSV Files/FinalExport2.csv")

"""
Dropping a few rows due to the following error:
KeyError: Invalid Country Alpha-2 code: 
Error remains unresolved as the correct alpha 2 code was assigned by the pc.country_name_to_country_alpha2 function.
This can be verified using print(list(pycountry.countries))
"""
df.drop(df.loc[df['country_code_alpha2'] == 'SX'].index, inplace=True)
df.drop(df.loc[df['country_code_alpha2'] == 'PN'].index, inplace=True)
df.drop(df.loc[df['country_code_alpha2'] == 'TL'].index, inplace=True)

# Converting country code to continent using pycountry.
df['continent'] = df.country_code_alpha2.apply(pc.country_alpha2_to_continent_code)

# Checking if read was successful and new collumns added to the df.
print(df.head())

# Split the data into smaller sub dataframes to allow for easier graph plotting.
africa = df[df["continent"] == 'AF']
# print(africa) - Uncomment to verify.

asia = df[df["continent"] == 'AS']
# print(asia) - Uncomment to verify.

oceania = df[df["continent"] == 'OC']
# print(oceania) - Uncomment to verify.

europe = df[df["continent"] == 'EU']
# print(europe) - Uncomment to verify.

northam = df[df["continent"] == 'NA']
# print(northam) - Uncomment to verify.

southam = df[df["continent"] == 'SA']
# print(southam) - Uncomment to verify.


# Plot horizontal bar chart
plot = px.data.tips()
fig = px.bar(asia, x="totalvaccinations", y="country", title="Total Vaccinations Administered in Africa",
             color="fullyvacnumber", text="totalvaccinations", labels=dict(totalvaccinations="Total Vaccinations (2 dose)", country="Country",
                                                 fullyvacnumber="Number of Fully Vaccinated", ), orientation='h')
fig.update_layout(barmode='group', yaxis={'categoryorder':'total ascending'})
fig.update_xaxes(type="log")

fig.show()


first_line = go.Bar(x=asia["totalvaccinations"], y=asia["country"], name="Total Vaccinations in Asia",
                    orientation='h', width=1.5)
second_line = go.Bar(x=africa["totalvaccinations"], y=africa["country"], name="Total Vaccinations in Africa",
                     orientation='h', width=1.5)
third_line = go.Bar(x=oceania["totalvaccinations"], y=oceania["country"], name="Total Vaccinations in Oceania",
                    orientation='h', width=1.5)

fig = make_subplots(rows=1, cols=3, shared_yaxes=True)
fig.add_trace(first_line, row=1, col=1)
fig.add_trace(second_line, row=1, col=2)
fig.add_trace(third_line, row=1, col=3)
fig.show()
# TODO: Group other sub dataframes into the bar chart.

# Built a Choropleth Map:

worldMap = px.choropleth(asia,
                title="World Map of Fully Vaccinated",
                locations ="isocode",
                color="fullyvacnumber",
                hover_name="country", # column to add to hover information
                color_continuous_scale=px.colors.sequential.Viridis,)
worldMap.update_layout(
    coloraxis_colorbar=dict(
        title="Number of Fully Vaccinated"))
worldMap.show()

# TODO: Group all  sub datasets into one aka, multiple pages of same graph outlining a different continent.