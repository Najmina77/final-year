import requests
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import itertools
import warnings
import datetime
import pickle
# Import the statsmodels library for using SARIMAX model
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose

warnings.filterwarnings("ignore") # specify to ignore warning messages

# get the current date in the format yyyddmm
# get the current date in the format yyyddmm
now_date = datetime.datetime.now() + datetime.timedelta(days=-3)
now_date_str = str(now_date)
now_date_split = now_date_str.split('-')
now_day = now_date_split[2].split(' ')[0]
now_date_only = '{}{}{}'.format(now_date_split[0], now_date_split[1], now_day)
now_date_only





#download data for embu, nyeri aand nanyuki as test cities

def get_embu_data_from_2021():
    day_data_url =  'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,WS2M,RH2M&community=AG&longitude=37.4596&latitude=-0.5388&start=20200101&end={}&format=JSON'.format(now_date_only)
    response = requests.get(day_data_url)
    day_data = response.content.decode('utf-8') 
    day_data = json.loads(day_data)
    properties = day_data['properties']
    parameters = properties['parameter']
    precipitation = parameters['RH2M'] #
    temp = parameters['T2M']
    wind = parameters['WS2M']
    
    return (precipitation, temp, wind)

def get_nyeri_data_from_2021():
    day_data_url =  'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,WS2M,RH2M&community=AG&longitude=36.9580&latitude=-0.4371&start=20200101&end={}&format=JSON'.format(now_date_only)
    response = requests.get(day_data_url)
    day_data = response.content.decode('utf-8') 
    day_data = json.loads(day_data)
    properties = day_data['properties']
    parameters = properties['parameter']
    precipitation = parameters['RH2M'] #
    temp = parameters['T2M']
    wind = parameters['WS2M']
    
    return (precipitation, temp, wind)


def get_nanyuki_data_from_2021():
    day_data_url =  'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,WS2M,RH2M&community=AG&longitude=37.0722&latitude=0.0074&start=20200101&end={}&format=JSON'.format(now_date_only)
    response = requests.get(day_data_url)
    day_data = response.content.decode('utf-8') 
    day_data = json.loads(day_data)
    properties = day_data['properties']
    parameters = properties['parameter']
    precipitation = parameters['RH2M'] #
    temp = parameters['T2M']
    wind = parameters['WS2M']   

    return (precipitation, temp, wind)

#get the rainfall, temperature and wind for each of the test cities
print('Downloading data for Nyeri, Embu and Nanyuki as test cities')
embu_precipitation, embu_temp, embu_wind = get_embu_data_from_2021()
nyeri_precipitation, nyeri_temp, nyeri_wind = get_nyeri_data_from_2021()
nanyuki_precipitation, nanyuki_temp, nanyuki_wind = get_nanyuki_data_from_2021()



#convert the dictionaries to lists to form dataframes later

#for Embu
embu_dates = []
embu_temp_values = []
embu_precipitation_values = []
embu_wind_values = []

for key, value in embu_precipitation.items():
    embu_dates.append(key)
    embu_precipitation_values.append(value)
    
for key, value in embu_temp.items():
    embu_temp_values.append(value)
    
for key, value in embu_wind.items():
    embu_wind_values.append(value)
    
#for Nyeri
nyeri_dates = []
nyeri_temp_values = []
nyeri_precipitation_values = []
nyeri_wind_values = []

for key, value in nyeri_precipitation.items():
    nyeri_dates.append(key)
    nyeri_precipitation_values.append(value)
    
for key, value in nyeri_temp.items():
    nyeri_temp_values.append(value)
    
for key, value in nyeri_wind.items():
    nyeri_wind_values.append(value)
    
    
#for Nanyuki
nanyuki_dates = []
nanyuki_temp_values = []
nanyuki_precipitation_values = []
nanyuki_wind_values = []

for key, value in nanyuki_precipitation.items():
    nanyuki_dates.append(key)
    nanyuki_precipitation_values.append(value)
    
for key, value in nanyuki_temp.items():
    nanyuki_temp_values.append(value)
    
for key, value in nanyuki_wind.items():
    nanyuki_wind_values.append(value)
    



# form dataframes, for use later in the project for processing the data

embu_df = pd.DataFrame()
embu_df['datetime'] = embu_dates
embu_df['precipitation'] = embu_precipitation_values
embu_df['temp'] = embu_temp_values
embu_df['wind'] = embu_wind_values

nyeri_df = pd.DataFrame()
nyeri_df['datetime'] = nyeri_dates
nyeri_df['precipitation'] = nyeri_precipitation_values
nyeri_df['temp'] = nyeri_temp_values
nyeri_df['wind'] = nyeri_wind_values

nanyuki_df = pd.DataFrame()
nanyuki_df['datetime'] = nanyuki_dates
nanyuki_df['precipitation'] = nanyuki_precipitation_values
nanyuki_df['temp'] = nanyuki_temp_values
nanyuki_df['wind'] = nanyuki_wind_values


#reset indexes to datetime
embu_df.set_index('datetime', inplace=True)
nyeri_df.set_index('datetime', inplace=True)
nanyuki_df.set_index('datetime', inplace=True)


#Embu
# Shift the current temperature to the next day. 
embu_predicted_df = embu_df.temp.to_frame().shift(1).rename(columns = {"temp": "temp_pred" })
embu_actual_df = embu_df.temp.to_frame().rename(columns = {"temp": "temp_actual" })

# Concatenate the actual and predicted temperature
embu_one_step_df = pd.concat([embu_actual_df, embu_predicted_df],axis=1)

# Select from the second row, because there is no prediction for today due to shifting.
embu_one_step_df = embu_one_step_df[1:]


#Nyeri
# Shift the current temperature to the next day. 
nyeri_predicted_df = nyeri_df.temp.to_frame().shift(1).rename(columns = {"temp": "temp_pred" })
nyeri_actual_df = nyeri_df.temp.to_frame().rename(columns = {"temp": "temp_actual" })

# Concatenate the actual and predicted temperature
nyeri_one_step_df = pd.concat([nyeri_actual_df, nyeri_predicted_df],axis=1)

# Select from the second row, because there is no prediction for today due to shifting.
nyeri_one_step_df = nyeri_one_step_df[1:]


#Nanyuki
# Shift the current temperature to the next day. 
nanyuki_predicted_df = nanyuki_df.temp.to_frame().shift(1).rename(columns = {"temp": "temp_pred" })
nanyuki_actual_df = nanyuki_df.temp.to_frame().rename(columns = {"temp": "temp_actual" })

# Concatenate the actual and predicted temperature
nanyuki_one_step_df = pd.concat([nanyuki_actual_df, nanyuki_predicted_df],axis=1)

# Select from the second row, because there is no prediction for today due to shifting.
nanyuki_one_step_df = nanyuki_one_step_df[1:]



# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]



#embu
# Fit the SARIMAX model using optimal parameters
print('Trainign the Embu weather Model')
embu_mod = sm.tsa.statespace.SARIMAX(embu_one_step_df.temp_actual,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

embu_results = embu_mod.fit()


#nyeri
# Fit the SARIMAX model using optimal parameters
print('Training the Nyeri waether Model')
nyeri_mod = sm.tsa.statespace.SARIMAX(nyeri_one_step_df.temp_actual,
                                order=(1, 1, 1),
                                  seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

nyeri_results = nyeri_mod.fit()


#nanyuki
# Fit the SARIMAX model using optimal parameters
print('Training the Nayuki weather Model')
nanyuki_mod = sm.tsa.statespace.SARIMAX(nanyuki_one_step_df.temp_actual,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

nanyuki_results = nanyuki_mod.fit()

print('Hoooooorey! Finished Training all the models, Now saving them')


embu_model_name = 'embu_weather_model'
nyeri_model_name = 'nyeri_weather_model'
nanyuki_model_name = 'nayuki_weather_model'

pickle.dump(embu_results, open(embu_model_name, 'wb'))
pickle.dump(nanyuki_results, open(nanyuki_model_name, 'wb'))
pickle.dump(nyeri_results, open(nyeri_model_name, 'wb'))

print('I just  saved the models and reached the end of the training, its time to do other things!')