#!/usr/bin/env python

from __future__ import print_function
import liblo, sys
import csv
import math
import copy
import bluetooth

# List of paths returned by muse app
paths = {
    '/muse/eeg':    0, 
    '/muse/gyro':   1, 
    '/muse/acc':    2, 
    '/muse/elements/touching_forehead':     3,
    '/muse/elements/alpha_absolute':        4,
    '/muse/elements/beta_absolute':         5,
    '/muse/elements/delta_absolute':        6,
    '/muse/elements/theta_absolute':        7,
    '/muse/elements/gamma_absolute':        8,
    '/muse/elements/horseshoe':             9,
    '/muse/elements/jaw_clench':            10,
}

# Accumulator to store the values of each band
Accu = {
    0: [0, 0, 0, 0, 0],
    1: [0, 0, 0],
    2: [0, 0, 0],
    3: [0],
    4: [0, 0, 0, 0],
    5: [0, 0, 0, 0],
    6: [0, 0, 0, 0],
    7: [0, 0, 0, 0],
    8: [0, 0, 0, 0],
    9: [0, 0, 0, 0]
}

# frequency of each feild in the accumulator
Freq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# create a copy for Accu and Freq
accu = copy.deepcopy(Accu)
freq = copy.deepcopy(Freq)

# the path value associated with forword movement
FORWARD = 10

# current motion category
MODE = -1

# list of motion
FRONT = 0
LEFT = 1
RIGHT = 2
STOP = 3

# command strings
command = {
    0: 'F',
    1: 'L',
    2: 'R',
    3: 'S'
}

# Bot mac address
BOT_ADDR = "00:21:13:04:32:5A"

# add server method to handle data
if __name__ == '__main__':

    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    for port in range(1, 100):
        try:
            sock.connect((BOT_ADDR, port))
            print('Connected to {} on port {}'.format(BOT_ADDR, port))
            break
        except bluetooth.btcommon.BluetoothError as e:
            print('{}'.format(e))

    try:
        while True:
            sock.send(command[3])
    except bluetooth.btcommon.BluetoothError as e:
        print('{}'.format(e))
        sock.close()
