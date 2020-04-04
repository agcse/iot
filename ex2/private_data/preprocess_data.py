#!/usr/bin/env python

import os
import pandas as pd

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

    pass
