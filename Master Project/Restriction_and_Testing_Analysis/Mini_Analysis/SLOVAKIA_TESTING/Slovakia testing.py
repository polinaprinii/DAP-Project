#!/usr/bin/env python
# coding: utf-8

# In[84]:

#Libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy


# In[55]:


#Reading the file
SlovakiaTesting=pd.read_csv("D:\Git\DAP-Project\Restriction and Testing Analysis\Mini Analysis\SLOVAKIA TESTING\SlovakiaTesting.csv",error_bad_lines=False, engine="python")


# In[65]:

#Removing NA values
SlovakiaTesting = SlovakiaTesting.dropna()


# In[125]:

#Creating the plot
fig = px.bar(SlovakiaTesting, x="Gender", y="PCRPos", color="Gender",facet_col="AgeGroup",template="plotly_white")


# In[ ]:

#Saving the plot
fig.write_html("D:\Git\DAP-Project\Restriction and Testing Analysis\Mini Analysis\SLOVAKIA TESTING\SlovakiaTesting.html")


# In[ ]:




