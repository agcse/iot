#!/usr/bin/env python

import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
def abspath(file):
    return os.path.join(CURR_DIR, file)

def show_map(m):
    plt.figure(figsize=(15,8))
    plt.imshow(m)
    plt.title('Tellus')
    plt.axis('off')
    plt.show()

def add_locations(m):
    locations = pd.read_csv(abspath('private_data/relative_locations.csv'))
    rows, cols, _ = m.shape

    y_coords = []
    for l in locations['latitude']:
        y_coords.append(round(l * rows))

    x_coords = []
    for l in locations['longitude']:
        x_coords.append(round(l * cols))

    y_correction = 7
    x_correction = -85
    for x, y in zip(x_coords, y_coords):
        m = cv2.circle(m, (x + x_correction, rows - y + y_correction), 1, (0, 0, 255))

    return m

if __name__ == '__main__':
    # reading and color convert to RGB
    tellus_map = cv2.imread(abspath('tellus_map.png'))
    tellus_map = cv2.cvtColor(tellus_map, cv2.COLOR_BGR2RGB)
    print(tellus_map.shape)

    # adding locations
    tellus_map = add_locations(tellus_map)

    # rendering
    show_map(tellus_map)
