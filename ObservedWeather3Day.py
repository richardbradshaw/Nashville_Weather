#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
import requests
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# In[2]:


# get the data from the url, then parse it as a DataFrame
url = 'https://w1.weather.gov/data/obhistory/KBNA.html'
r = requests.get(url)
df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
data = df_list[3]
data = data.iloc[:-3]


# In[3]:


# Remove the first two column header levels, then rename the remaining columns
data.columns = data.columns.droplevel([0,1])
data = data.rename(columns = {'Air':'AirTemp','Max.':'6hourMaxTemp','Min.':'6hourMinTemp','1 hr':'1hrPrecip','3 hr':'3hrPrecip','6 hr':'6hrPrecip','RelativeHumidity':'RelativeHumidity(%)'})


# In[4]:


from datetime import date, datetime, timedelta
from dateutil import tz
retrievalDate = date.today()


# In[5]:


# Change numerical values to floats
data[['Date', 'Vis.(mi.)', 'AirTemp', 'Dwpt', '6hourMaxTemp', '6hourMinTemp',
       'WindChill(°F)', 'HeatIndex(°F)', 'altimeter(in)', 'sea level(mb)',
       '1hrPrecip', '3hrPrecip', '6hrPrecip']] = data[['Date', 'Vis.(mi.)', 'AirTemp', 'Dwpt', '6hourMaxTemp', '6hourMinTemp',
       'WindChill(°F)', 'HeatIndex(°F)', 'altimeter(in)', 'sea level(mb)',
       '1hrPrecip', '3hrPrecip', '6hrPrecip']].astype('float')


# In[6]:


data['RelativeHumidity(%)'] = data['RelativeHumidity(%)'].str.strip('%')
data['RelativeHumidity(%)'] = data['RelativeHumidity(%)'].astype('float')


# In[7]:


# Code to create the date offsets to correctly assign the actual datetimes

# get unique dates
dateUnique = data['Date'].unique()

# get offsets for each unique date
offsets = list(range(len(dateUnique)))

# create dictionary
offsetDict = dict(zip(list(dateUnique), offsets))

# assign the dateOffset column to the values in the Date column
data['dateOffset'] = data['Date']

# replace the dateOffset values to the offsets in the offsetDict
data['dateOffset'] = data['dateOffset'].replace(offsetDict)


# In[8]:


# Create column of the retrieval Date
data['retrievalDate'] = retrievalDate
data['retrievalDate'] = pd.to_datetime(data['retrievalDate'])

# Subtract the dateOffset from the retrieval date to get the full date of the observations
data['dateRel'] = pd.DatetimeIndex(data['retrievalDate']) - pd.to_timedelta(data['dateOffset'], unit='D')

# Combine the date and time
data['dateTime'] = pd.to_datetime(data['dateRel'].astype(str) + data['Time(cdt)'], format = '%Y-%m-%d%H:%M')


# In[9]:


# Saving data

from os import path
filename = 'observedWeatherNash.csv'

# Check if output file exists
if path.exists(filename):
    oldData = pd.read_csv('observedWeatherNash.csv')
    dataAll = data.append(oldData, sort=False)
    # remove duplicates
    dataAll.drop_duplicates(subset=['Date', 'Time(cdt)', 'Wind(mph)', 'Vis.(mi.)', 'Weather', 'Sky Cond.',
           'AirTemp', 'Dwpt', 'altimeter(in)', 'sea level(mb)'], inplace=True)
    # Save dataAll
    dataAll.to_csv(filename, index=False)
else:
    # Save initial data to file
    data.to_csv(filename, index=False)

