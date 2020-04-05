#!/usr/bin/env python

import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


# constants
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
POINT_RADIUS = 1
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'  # without microseconds
Y_CORRECTION = 7
X_CORRECTION = -85


def abspath(file):
    return os.path.join(CURR_DIR, file)


def add_locations(m):
    """Adds sensor locations to the map, returns new map and locations"""
    locations = pd.read_csv(abspath('private_data/relative_locations.csv'))
    rows, cols, _ = m.shape

    y_coords = []
    for l in locations['latitude']:
        y_coords.append(round(l * rows))

    x_coords = []
    for l in locations['longitude']:
        x_coords.append(round(l * cols))

    for x, y in zip(x_coords, y_coords):
        m = cv2.circle(m, (x + X_CORRECTION, rows - y + Y_CORRECTION), POINT_RADIUS, (0, 0, 255),
            thickness=cv2.FILLED)

    # parse locations into dict
    device_locations = {}
    for _, row in locations.iterrows():
        device_locations[row['id']] = (rows - round(row['latitude'] * rows), round(row['longitude'] * cols))

    return m, device_locations


def to_datetime(ts):
    ts = ts.split('.')
    dt = datetime.strptime(ts[0], DATETIME_FORMAT)
    if len(ts) == 1:  # no microseconds
        return dt
    if ts[1] == '':  # empty microseconds but '.' exists
        return dt
    microsec = int(ts[1]) * 1000
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, microsec)


def get_data(dt=None):
    data = pd.read_csv(
        abspath('private_data/data.csv'), dtype={'id': str, 'timestamp': str, 'pir': np.int32})
    data['timestamp'] = data['timestamp'].map(lambda ts: to_datetime(ts))
    if dt is None:
        return data
    dt_first, dt_last = dt
    return data.loc[(data['timestamp'] >= dt_first) & (data['timestamp'] <= dt_last)]


def add_pir(m, data, device_locations):
    pirs = {}
    for _, row in data.iterrows():
        device = row['id']
        pir = pirs.get(device, 0) + row['pir']
        if (pir == 0):
            continue
        locations = device_locations.get(device)
        if locations is None:
            print('id not found in locations CSV:', device)
            continue
        y, x = locations  # get latitude, longitude
        m = cv2.circle(m, (x + X_CORRECTION, y + Y_CORRECTION), POINT_RADIUS + pir, (255, 0, 255),
            thickness=cv2.FILLED)
        pirs[device] = pir
    return m


def show_map(m):
    plt.figure(figsize=(15,8))
    plt.imshow(m)
    plt.title('Tellus')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    # reading and color convert to RGB
    tellus_map = cv2.imread(abspath('tellus_map.png'))
    tellus_map = cv2.cvtColor(tellus_map, cv2.COLOR_BGR2RGB)

    # add locations
    tellus_map, locations = add_locations(tellus_map)

    # get data
    dt_first = to_datetime('2018-01-27 19:08:28.428')
    dt_last = to_datetime('2018-01-27 19:11:51.48')
    data = get_data((dt_first, dt_last))

    # add sensor data
    tellus_map = add_pir(tellus_map, data, locations)

    # rendering
    show_map(tellus_map)
