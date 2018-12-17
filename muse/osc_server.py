#!/usr/bin/env python

from __future__ import print_function
import liblo, sys
import csv
import math
import copy

# A list of port to connect
ports = []
for port in range(5000, 6000, 50):
    ports.append(port)

# Try to establish connection to a port
for port in ports:
    try:
        server = liblo.Server(port)
        print('Connected to Port {}'.format(port))
        break
    except Error as err:
        print(err)
        sys.exit()

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
    '/muse/elements/horseshoe':             9
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
# sr_no_ct is csv file serial number
accu = copy.deepcopy(Accu)
freq = copy.deepcopy(Freq)
sr_no_ct = 1

# assign values from accumulator to the feild.
# This is used to write data in csv file
def make_dict():
    data = {
        'No': sr_no_ct, 
        'RAW_TP9': accu[0][0], 
        'RAW_AF7': accu[0][1], 
        'RAW_AF8': accu[0][2], 
        'RAW_TP10': accu[0][3], 
        'REF': accu[0][4], 
        'Accelerometer_X': accu[2][0], 
        'Accelerometer_Y': accu[2][1], 
        'Accelerometer_Z': accu[2][2], 
        'Gyro_X': accu[1][0], 
        'Gyro_Y': accu[1][1], 
        'Gyro_Z': accu[1][2], 
        'Alpha_TP9': accu[4][0],
        'Alpha_AF7': accu[4][1],
        'Alpha_AF8': accu[4][2],
        'Alpha_TP10': accu[4][3],
        'Beta_TP9': accu[5][0],
        'Beta_AF7': accu[5][1],
        'Beta_AF8': accu[5][2],
        'Beta_TP10': accu[5][3],
        'Delta_TP9': accu[6][0],
        'Delta_AF7': accu[6][1],
        'Delta_AF8': accu[6][2],
        'Delta_TP10': accu[6][3],
        'Theta_TP9': accu[7][0],
        'Theta_AF7': accu[7][1],
        'Theta_AF8': accu[7][2],
        'Theta_TP10': accu[7][3],
        'Gamma_TP9': accu[8][0],
        'Gamma_AF7': accu[8][1],
        'Gamma_AF8': accu[8][2],
        'Gamma_TP10': accu[8][3]
    }

    return data

# check if the current values of the accu 
# feild are valid.
def validate():
    if 0 in freq:
        return False

    for key in accu.keys():
        tot = 0
        for data in accu[key]:
            tot += abs(data)
        if tot == 0:
            return False

    return True

# handler for incoming data
def fallback(path, args, types, src):
    print("path: {}".format(path))
    print("args: {}".format(args))
    print()

    global freq, accu, sr_no_ct

    if path not in paths.keys():
        print('error: invalid path: {}'.format(path))
        return
    msg_type = paths[path]

    # nan and inf or -inf are result of improper
    # sensor connection, so ignore those values
    for num in args:
        if math.isnan(num) or math.isinf(abs(num)):
            return

    freq[msg_type] += 1
    for idx in range(len(accu[msg_type])):
        accu[msg_type][idx] += args[idx]

    # this is an entry point for data calculation.
    # in each cycle it occurs only ones
    if (msg_type == 9):
        if not validate():
            accu = copy.deepcopy(Accu)
            freq = copy.deepcopy(Freq)
            return
        
        # normalise the values based on freq
        for ele in range(10):
            for idx in range(len(accu[ele])):
                accu[ele][idx] /= freq[ele]
        
        data = make_dict()
        writer.writerow(data)
        
        print('Data:')
        print(accu)

        sr_no_ct += 1
        accu = copy.deepcopy(Accu)
        freq = copy.deepcopy(Freq)

    return

# add server method to handle data
server.add_method(None, None, fallback)

with open('muse_eeg_data.csv', 'w') as csvfile:
    fieldnames = [
        'No', 
        'RAW_TP9', 
        'RAW_AF7', 
        'RAW_AF8', 
        'RAW_TP10', 
        'REF', 
        'Accelerometer_X', 
        'Accelerometer_Y', 
        'Accelerometer_Z', 
        'Gyro_X', 
        'Gyro_Y', 
        'Gyro_Z', 
        'Alpha_TP9',
        'Alpha_AF7',
        'Alpha_AF8',
        'Alpha_TP10',
        'Beta_TP9',
        'Beta_AF7',
        'Beta_AF8',
        'Beta_TP10',
        'Delta_TP9',
        'Delta_AF7',
        'Delta_AF8',
        'Delta_TP10',
        'Theta_TP9',
        'Theta_AF7',
        'Theta_AF8',
        'Theta_TP10',
        'Gamma_TP9',
        'Gamma_AF7',
        'Gamma_AF8',
        'Gamma_TP10'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    while True:
        server.recv(1000)
