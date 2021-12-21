#!/usr/bin/env python
# coding: utf-8

# In[21]:

#Libraries
import pandas as pd
import plotly.graph_objects as go


# In[24]:

#Reading the file
IrelandSlovakia = pd.read_csv("D:\Git\DAP-Project\Restriction and Testing Analysis\Mini Analysis\RESTRICTIONS\IrelandSlovakiastringency.csv")
IrelandSlovakia


# In[37]:

#Creating the plot
fig = px.area(
    IrelandSlovakia, 
    x = 'Day',
    y = 'stringency_index',
    color='Entity',
    title = 'Stringency Index by date for Ireland and Slovakia'
)


# In[38]:


fig


# In[40]:

#Saving the plot
fig.write_image("D:\Git\DAP-Project\Restriction and Testing Analysis\Mini Analysis\RESTRICTIONS\IrelandSlovakia.png")


# In[42]:


fig.write_html("D:\Git\DAP-Project\Restriction and Testing Analysis\Mini Analysis\RESTRICTIONS\IrelandSlovakia.html")


# In[ ]:




