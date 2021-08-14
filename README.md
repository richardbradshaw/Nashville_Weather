# Nashville_Weather

Ongoing analysis of weather forecast and observed weather data from the National Weather Service for Nashville, Tennessee. I am interested in visualizing the accuracy and precision of weather forecasts. The data used in the analysis is retrieved from the National Weather Service office (KBNA) in Nashville, Tennessee. 

There are three python files: NWS_API.py, ObservedWeather3Day.py, and ForecastAnalysis.ipynb. 

The NWS_API.py file retrieves the weather forecast data from the NWS api. It retrieves both the daily and hourly forecasts. Initially, I am only using the daily forecasts, but can eventually analyze the hourly forecasts.

The ObservedWeather3Day.py file retrieves the actual weather observations from the weather station located at the Nashville International Airport. This data is scraped from the NWS website, because the observations are not included in the current version of the api.

Both the NWS_API and ObservedWeather3Day scripts are run every morning on my personal computer, scheduled using crontab.

The ForecastAnalysis.ipynb is a Jupyter notebook where the data analysis is performed. The objective of this analysis is to compare the weather forecasts with the actual observations to assess the accuracy and precision of the forecasts to test how forecast accuracy or precision changes with time of forecast (i.e., how accurate and precise is the forecast for today, versus the forecast for 7 days from now). 
