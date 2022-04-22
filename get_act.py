# a script to load some figures of my gps data

import pandas as pd
import numpy as np
import os, glob
import re

# getting a list of files
csv_files = []
os.chdir('/Users/kylekent/Library/CloudStorage/Dropbox/cycling_analytics/strava_export_04-15-22/activities/')
for file in glob.glob('*.csv'):
    csv_files.append(file)

# now lets organize them by date with the newest rides coming first
csv_files = sorted(csv_files, key = str.lower, reverse = True)

# and lets load only the rides from 2020
# _2020 = [f for f in csv_files if re.match('.{8}2020.*', f)] # this works but I made the following for loop
_2020 = []
for f in enumerate(csv_files):
    if bool(re.match('.{8}2020.*', f[1])):
        _2020.append(f[1])

# now lets load each file as a df inside a dictionary with the file names
loaded_files = {}
for i in range(len(_2020)):
    f = open(_2020[i], 'r')
    loaded_files[_2020[i]] = pd.read_csv(f)
    f.close()

# we can also append them onto one large df with the file names as a column
col_names = list(list(loaded_files.values())[0].columns)
col_names.append('load_index')

df_2020 = pd.DataFrame(columns = col_names)
for i in range(len(_2020)):
    f = open(_2020[i], 'r')
    df = pd.read_csv(f)
    df['load_index'] = i
    df_2020 = df_2020.append(df)
    f.close()
df_2020 = df_2020.reset_index(drop = True)

# lets add some useful time columns
df_2020['timestamp'] = pd.to_datetime(df_2020['timestamp'], utc = True).dt.tz_convert(tz = 'America/Chicago')
df_2020['time'] = pd.to_datetime(df_2020['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S'))
df_2020['year'] = df_2020['timestamp'].dt.strftime('%Y')
df_2020['month'] = df_2020['timestamp'].dt.strftime('%m')
df_2020['day'] = df_2020['timestamp'].dt.strftime('%d')

# lets add some useful information columns
    # first average speed
avg_speed = df_2020.groupby('load_index', as_index = False)['enhanced_speed'].mean()
avg_speed.columns.values[1] = 'avg_speed'
df_2020 = df_2020.join(avg_speed, on = 'load_index', rsuffix = '_del')
del df_2020['load_index_del']

    # now elevation gain
df_2020['elevation_change'] = df_2020['altitude'].diff() # get elevation differences
df_2020.loc[~df_2020['load_index'].eq(df_2020['load_index'].shift()), 'elevation_change'] = np.nan # make sure the first row of each ride is NA

df_2020['elevation_gain'] = df_2020['elevation_change']
df_2020.loc[df_2020['elevation_change'] < 0, 'elevation_gain'] = 0 # make all the negative elevation changes a 0 for gain

# filtering datetime object
    # using query for datetime formats
#df_2020.query('2020 <= isotime')
    # using indexing for string columns
df_2020[df_2020['year'] == '2020']

# getting figures of df_2020
df_2020[df_2020['load_index'] == 0].plot('position_lat', 'position_long', color = 'red', linewidth = 1.5)
df_2020[df_2020['load_index'] == 1].plot('position_lat', 'position_long', color = 'red', linewidth = 1.5)
df_2020[df_2020['load_index'] == 2].plot('position_lat', 'position_long', color = 'red', linewidth = 1.5)

# this is all great, but let's get a df with all the data present in the activities directory
# here's a function to get all the files loaded into a df
def get_csv_files():
    # getting csv file names
    csv_files = []
    os.chdir('/Users/kylekent/Library/CloudStorage/Dropbox/cycling_analytics/strava_export_04-15-22/activities/')
    for file in glob.glob('*.csv'):
        csv_files.append(file)
    # ordering the list
    csv_files = sorted(csv_files, key=str.lower, reverse=True)
    # setting up the df
    col_names = ['timestamp', 'position_lat', 'position_long', 'distance', 'enhanced_altitude', 'altitude', 'enhanced_speed', 'speed', 'heart_rate', 'cadence', 'fractional_cadence', 'temperature', 'file_index']
    df = pd.DataFrame(columns = col_names)
    for i in range(len(csv_files)):
        f = open(csv_files[i], 'r')
        dft = pd.read_csv(f)
        dft['file_index'] = i
        df = df.append(dft)
        f.close()
    # resetting the index
    df = df.reset_index(drop=True)
    return df

# load all csv files into one
all_rides = get_csv_files()

# adding date columns
all_rides['timestamp'] = pd.to_datetime(all_rides['timestamp'], utc = True).dt.tz_convert(tz = 'America/Chicago')
all_rides['date'] = pd.to_datetime(all_rides['timestamp'].dt.strftime('%Y-%m-%d'))
all_rides['year'] = all_rides['timestamp'].dt.strftime('%Y')
all_rides['month'] = all_rides['timestamp'].dt.strftime('%m')

# getting variables to compare speed and elevation
avg_speed = all_rides.groupby('file_index', as_index = False)['enhanced_speed'].mean()
avg_speed.columns.values[1] = 'avg_speed'
all_rides = all_rides.join(avg_speed, on = 'file_index', rsuffix = '_del')
print('delete index')
del avg_speed

all_rides['elevation_change'] = all_rides['enhanced_altitude'].diff() # get elevation differences
all_rides.loc[~all_rides['file_index'].eq(all_rides['file_index'].shift()), 'elevation_change'] = np.nan # make sure the first row of each ride is NA
all_rides['elevation_gain'] = all_rides['elevation_change']
all_rides.loc[all_rides['elevation_change'] < 0, 'elevation_gain'] = 0

# switching columns order
col_list = all_rides.columns.to_list()
col_ordered = [col_list[12]] + [col_list[0]] + [col_list[13]] + [col_list[16]] + [col_list[-1]] + col_list[1:12] + col_list[14:16] + [col_list[17]]
all_rides = all_rides[col_ordered]

# let's get this into a smaller averaged out dataset
# to get descriptive stats on some measures we need to change dtypes
all_rides = all_rides.replace('None', np.nan)
all_rides = all_rides.fillna(value = np.nan)
all_rides = all_rides.astype({'distance':'float64'})
all_rides = all_rides.astype({'heart_rate':'float64'})
# lets write it to a csv for future use
all_rides.dtypes.apply(lambda x: x.name).to_dict()
print(all_rides)
all_rides.to_csv('/Users/kylekent/Library/CloudStorage/Dropbox/cycling_analytics/all_rides.csv.gz', index = False, compression = 'gzip')
print('written')
# now we can get descriptive stats
all_rides_avgs = all_rides.groupby('file_index', as_index = False).agg({'elevation_gain':'sum', \
                                                                        'avg_speed':'mean', \
                                                                        'distance':'max', \
                                                                        'heart_rate': 'mean'})
all_rides_avgs['date'] = all_rides.groupby('file_index')['date'].unique()
all_rides_avgs['year'] = all_rides.groupby('file_index')['year'].unique()
all_rides_avgs['month'] = all_rides.groupby('file_index')['month'].unique()
all_rides_avgs.dtypes.apply(lambda x: x.name).to_dict()
all_rides_avgs.to_csv('/Users/kylekent/Library/CloudStorage/Dropbox/cycling_analytics/all_rides_avgs.csv.gz', index = False, compression = 'gzip')

# plotting gps data
preCollege = all_rides.loc[(all_rides['year'] <= 2016) & (all_rides['year'] >= 2012) & (all_rides['file_index'] <= 265)]
preC_grouped = preCollege.groupby('file_index')

fig, ax1 = plt.subplots()
fig.hold(True)

preC_grouped.plot('position_lat', 'position_long', alpha = .7, fig = fig, ax = ax1)
plt.clf()

#
