import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import pandas as pd


data = pd.read_csv(
    'A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\CONVENIENT_global_confirmed_cases.csv',
    dtype='unicode')

data2 = pd.read_csv('A:\College\DAP-Project\Cases_and_Death_Rates\Data\Raw Data for EDA\CONVENIENT_global_deaths.csv',
                  dtype='unicode')


data.dropna(axis=0,inplace=True)
data2.dropna(axis=0,inplace=True)

data['Country/Region']=pd.to_datetime(data['Country/Region'])
data2['Country/Region']=pd.to_datetime(data2['Country/Region'])

# Create figure
fig = go.Figure()

# Add traces, one for each slider step
for step in data.columns.values[1:]:
    fig.add_trace(
        go.Scatter(
            visible=True,
            line=dict(width=2),
            name="Confirmed cases in " + step,
            x=data['Country/Region'],
            y=data[step].values,
            marker=dict(color=[i for i in range(len(data2.columns.values[1:]))])))

steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Slider switched to country: " + data.columns.values[1:][i]}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)
sliders = [dict(
    active=100,
    currentvalue={"prefix": "Frequency: "},
    steps=steps
)]

fig.update_layout(
    title_text="Change The Slider To Change To Different Countries",

    sliders=sliders
)

fig.show()