#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
# get_ipython().run_line_magic('matplotlib', 'inline')
import re
from time import sleep

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# In[2]:


from datetime import datetime
#from dateutil import tz
retrievalDate = datetime.today()
retrievalDate = retrievalDate.replace(minute=0, second=0, microsecond=0)


# In[3]:


# get data from NWS API
url = 'https://api.weather.gov/points/36.0680,-86.7475'
r = requests.get(url)
json_data = r.json()


# In[4]:


# Get forecast data
# forecast = json_data['properties']['forecast']
# r_Forecast = requests.get(forecast)
# json_data_forecast = r_Forecast.json()
# forecast_df = pd.DataFrame(json_data_forecast['properties']['periods'])

# Patch to fix common error: KeyError: 'properties'
for x in range(5):
    try:
        forecast = json_data['properties']['forecast']
        r_Forecast = requests.get(forecast)
        json_data_forecast = r_Forecast.json()
        forecast_df = pd.DataFrame(json_data_forecast['properties']['periods'])
        str_error = None
    except: #Exception as str_error:
        str_error = 1
        pass
    
    if str_error:
        sleep(2)
        #print('error')
    else:
        break


# In[6]:


# r_current = requests.get('https://api.weather.gov/stations/OHX/observations')
# json_data_current = r_current.json()


# In[8]:


# Get hourly forecast data
hourly_forecast = json_data['properties']['forecastHourly']
r_hourly = requests.get(hourly_forecast)
json_data_hourly = r_hourly.json()
hourly_df = pd.DataFrame(json_data_hourly['properties']['periods'])


# In[10]:


# convert ISO 8601 dates to normal (naive) DateTime 
hourly_df['startTime'] = pd.to_datetime(hourly_df['startTime']).dt.tz_localize(None)
hourly_df['endTime'] = pd.to_datetime(hourly_df['endTime']).dt.tz_localize(None)

forecast_df['startTime'] = pd.to_datetime(forecast_df['startTime']).dt.tz_localize(None)
forecast_df['endTime'] = pd.to_datetime(forecast_df['endTime']).dt.tz_localize(None)


# Extract the % chance of precipitation from the detailedForecast. 
# 
# Use regex: re.search() to extract the numerical text in a for loop

# In[11]:


# Extract precipitation forecast from detailedForecast string

precip = []

for text in forecast_df['detailedForecast']:
    if 'Chance of precipitation' in text:
        m = re.search('Chance of precipitation is (.+?)%', text)
        precip += [m.group(1)]
    else:
        precip += '0'
        

forecast_df['precip%'] = precip
forecast_df['precip%'] = forecast_df['precip%'].astype('int')


# In[30]:


# Extract wind speed forecast from windSpeed column (remove 'MPH' and assign to max and min)

wind = []
for data in forecast_df['windSpeed']:
    wind += [re.findall('[0-9]+', data)]

wind_df = pd.DataFrame(wind, columns=['windSpeedMin', 'windSpeedMax'])
forecast_df['windSpeedMin'] = wind_df['windSpeedMin'].astype('float')
forecast_df['windSpeedMax'] = wind_df['windSpeedMax'].astype('float')

nullWind = pd.isna(forecast_df['windSpeedMax'])
forecast_df.loc[nullWind, 'windSpeedMax'] = forecast_df.loc[nullWind, 'windSpeedMin']
forecast_df.loc[nullWind, 'windSpeedMin'] = 0


windHourly = []
for data in hourly_df['windSpeed']:
    windHourly += re.findall('[0-9]+', data)
    
hourly_df['wind'] = windHourly
hourly_df['wind'] = hourly_df['wind'].astype('float')


# In[13]:


# Add column of the retrieval date to both df
forecast_df['retrievalDate'] = retrievalDate
hourly_df['retrievalDate'] = retrievalDate


# In[14]:


# Save or append the data

from os import path
forecastFilename = 'forecastNash.csv'
hourlyFilename = 'hourlyForecastNash.csv'

# Check if output file exists
if path.exists(forecastFilename):
    oldForecast = pd.read_csv('forecastNash.csv')
    oldHourly = pd.read_csv('hourlyForecastNash.csv')
    forecast_out = pd.concat([oldForecast, forecast_df], ignore_index=True, sort=False)
    hourly_out = pd.concat([oldHourly, hourly_df], ignore_index=True, sort=False)
    
    forecast_out.to_csv(forecastFilename, index=False)
    hourly_out.to_csv(hourlyFilename, index=False)
    #forecast_df.to_csv(forecastFilename, mode='a', header=False, index=False)
    #hourly_df.to_csv(hourlyFilename, mode='a', header=False, index=False)
else:
    # Save initial data to file
    forecast_df.to_csv(forecastFilename, index=False)
    hourly_df.to_csv(hourlyFilename, index=False)


# In[22]:





# In[42]:





# In[ ]:




