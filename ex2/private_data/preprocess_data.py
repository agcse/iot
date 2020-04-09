#!/usr/bin/env python

import os
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
def abspath(file):
    return os.path.join(CURR_DIR, file)

if __name__ == '__main__':
    # data.csv:
    # data = pd.read_csv(abspath('data.csv'), sep=',')
    # data.drop(['co2', 'humidity', 'light', 'temperature'], axis=1, inplace=True)
    # data.to_csv(abspath('data.csv'))


    # locations.csv:
    # locations = pd.read_csv(abspath('locations.csv'), sep=';')
    # locations = locations[['id', 'locations', 'latitude', 'longitude']]
    # locations['id'] = locations['id'].map(
    #     lambda idstr: '-'.join(a + b for a,b in zip(idstr[::2], idstr[1::2])).lower())
    # locations.to_csv(abspath('locations.csv'))


    # 2nd part of locations.csv preprocessing:
    # corners = []
    # with open(abspath('map_corners.csv'), 'r') as corners_file:
    #     line = corners_file.readline()  # skip first line
    #     line = corners_file.readline()
    #     corners = [float(e) for e in line.split(',')]
    # latitudes = corners[::2]
    # longitudes = corners[1::2]
    # min_latitude, max_latitude = min(latitudes), max(latitudes)
    # min_longitude, max_longitude = min(longitudes), max(longitudes)

    # locations = pd.read_csv(abspath('locations.csv'), sep=',')
    # locations['latitude'] = locations['latitude'].map(
    #     lambda x: (x - min_latitude) / (max_latitude - min_latitude))
    # locations['longitude'] = locations['longitude'].map(
    #     lambda x: (x - min_longitude) / (max_longitude - min_longitude))
    # locations.to_csv(abspath('relative_locations.csv'))

    # removing index columns
    # import fileinput
    # for line in fileinput.input(files=[
    #         # abspath('data.csv'),
    #         # abspath('locations.csv'),
    #         abspath('relative_locations.csv')
    #     ], inplace=True, backup='.bak'):
    #     line = ','.join([e for e in line.strip().split(',')[1:]])
    #     print(line)

    # split data into monthly data
    # DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'  # without microseconds
    # def to_datetime(ts):
    #     ts = ts.split('.')
    #     dt = datetime.strptime(ts[0], DATETIME_FORMAT)
    #     if len(ts) == 1:  # no microseconds
    #         return dt
    #     if ts[1] == '':  # empty microseconds but '.' exists
    #         return dt
    #     microsec = int(ts[1]) * 1000
    #     return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, microsec)

    # def get_data():
    #     data = pd.read_csv(
    #         abspath('data.csv'), dtype={'id': str, 'timestamp': str, 'pir': np.int32})
    #     data['timestamp'] = data['timestamp'].map(lambda ts: to_datetime(ts))
    #     return data

    # def slice_data(data, dt):
    #     dt_first, dt_last = dt
    #     return data.loc[(data['timestamp'] >= dt_first) & (data['timestamp'] < dt_last)]

    # data = get_data()
    # start, end = data.iloc[0,:]['timestamp'], data.iloc[-1,:]['timestamp']
    # day_iters = int(abs((end - start).days) / 31) + 2
    # print(day_iters)

    # start = to_datetime('2017-06-26 10:26:02.779')
    # start = datetime(start.year, start.month, 1)
    # for _ in range(day_iters):
    #     end = (start + timedelta(days=31)).replace(day=1)
    #     print(start, end)
    #     slice_data(data, (start, end)).to_csv(
    #         abspath('data/data_' + str(start.year) + '_' + str(start.month) + '.csv'))
    #     start = end

    pass
