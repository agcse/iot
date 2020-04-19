#!/usr/bin/env python

import os
import sys
from datetime import datetime, timedelta

import cv2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import imageio


# constants
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
POINT_RADIUS = 1
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'  # without microseconds
Y_CORRECTION = 0
X_CORRECTION = -115


def abspath(file):
    return os.path.join(CURR_DIR, file)


def add_locations(m):
    """Adds sensor locations to the map, returns new map and locations"""
    locations = pd.read_csv(abspath('private_data/relative_locations.csv'))
    rows, cols, _ = m.shape

    rows += 0
    cols += 112

    device_locations = {}
    for _, row in locations.iterrows():
        y_coord = rows - round(row['latitude'] * rows) + Y_CORRECTION
        x_coord = round(row['longitude'] * cols) + X_CORRECTION
        device_locations[row['id']] = (y_coord, x_coord)
        m = cv2.circle(m, (x_coord, y_coord), POINT_RADIUS, (0, 0, 255), thickness=cv2.FILLED)

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
    """
    Returns data.csv as pandas.DataFrame.
    If dt is not None, frame slice is returned for dates [dt[0], dt[1]).
    """
    pdtype = {'id': str, 'timestamp': str, 'pir': np.int32}
    def get_all_data(dt):
        return pd.read_csv(abspath('private_data/data.csv'), dtype=pdtype, engine='c')
    def get_some_data(dt):
        return pd.read_csv(
            abspath('private_data/data/data_' + str(dt.year) + '_' + str(dt.month) + '.csv'),
            dtype=pdtype, engine='c')
    get_selector = { True: get_all_data, False: get_some_data }
    data = get_selector[(dt is None)](dt)
    data['timestamp'] = data['timestamp'].map(lambda ts: to_datetime(ts))
    return data


def slice_data(data, dt):
    dt_first, dt_last = dt
    return data.loc[(data['timestamp'] >= dt_first) & (data['timestamp'] < dt_last)]


def add_pir(m, data, device_locations):
    pirs = {}
    m_with_pir = np.copy(m)
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
        m_with_pir = cv2.circle(m_with_pir, (x, y), POINT_RADIUS + pir, (255, 0, 255),
            thickness=cv2.FILLED)
        m_with_pir = cv2.circle(m_with_pir, (x, y), POINT_RADIUS + pir, (0, 0, 0),
            thickness=1)
        pirs[device] = pir

    min_pir = 0
    max_pir = 0
    avg_pir = 0
    if pirs:
        min_pir = min(pirs.values())
        max_pir = max(pirs.values())
        avg_pir = round(sum(pirs.values()) / len(pirs))

    alpha = 0.5
    # alpha blend background with circles
    m_with_pir = cv2.addWeighted(m, alpha, m_with_pir, (1.0 - alpha), 0.0)
    return m_with_pir, (min_pir, max_pir, avg_pir)


def date_dayrange(start):
    return [start + timedelta(hours=hour) for hour in range(0, 25)]


def trivial_no_skip(v):
    return False


def date_range(start, end, delta_function, skip_function=trivial_no_skip):
    dt = start
    dates = []
    while dt >= start and dt <= end:
        curr = dt
        dt = dt + delta_function()
        if skip_function(curr):  # skip date according to function
            continue
        dates.append(curr)
    return dates


def show_map(m):
    plt.figure(figsize=(15,8))
    plt.imshow(m)
    plt.title('Tellus')
    plt.axis('off')
    plt.show()


def save_as_gif(images):
    imageio.mimwrite(abspath('tellus_pir.gif'), images, duration=1.0)


def save_as_avi(images):
    shape = images[0].shape
    writer = cv2.VideoWriter(abspath('tellus_pir.avi'), 0, 1, (shape[1], shape[0]))
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        writer.write(image)
    writer.release()


if __name__ == '__main__':
    # reading and color convert to RGB
    tellus_map = cv2.imread(abspath('tellus_map.png'))
    tellus_map = cv2.cvtColor(tellus_map, cv2.COLOR_BGR2RGB)

    # add locations
    tellus_map, locations = add_locations(tellus_map)

    # get data
    dt_start = to_datetime('2018-08-01 07:00:00')
    dt_end = to_datetime('2018-09-01 07:00:00')
    dates = date_range(dt_start, dt_end, lambda: timedelta(hours=4),
        lambda x: x.hour < 7 or x.hour > 22)

    # get full data
    data = get_data(dt_start)

    images = []
    for dt_first, dt_last in zip(dates, dates[1:]):
        data_slice = slice_data(data, (dt_first, dt_last))
        # add sensor data
        image, stats = add_pir(tellus_map, data_slice, locations)
        # add timestamp text
        image = cv2.copyMakeBorder(image, 80, 0, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        time_str = str(dt_first) + ' - ' + str(dt_last)
        image = cv2.putText(image, time_str, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        min_pir, max_pir, avg_pir = stats
        pir_str = 'MIN: ' + str(min_pir) + ' | MAX: ' + str(max_pir) + ' | AVG: ' + str(avg_pir)
        image = cv2.putText(image, pir_str, (0, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        # append to gif image array
        images.append(image)

    # save_as_gif(images)

    save_as_avi(images)

    # rendering
    # show_map(tellus_map)
