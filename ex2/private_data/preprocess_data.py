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

    pass
