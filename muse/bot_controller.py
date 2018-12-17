#!/usr/bin/env python

from __future__ import print_function
import liblo, sys
import csv
import math
import copy
import bluetooth
import numpy as np

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
LEFT_LIM = -0.8
RIGHT_LIM = 0.8
COUNT = 0

# command strings
command = {
    0: 'F',
    1: 'L',
    2: 'R',
    3: 'S'
}

# Bot mac address
BOT_ADDR = "00:21:13:04:32:5A"


# return x / (1 + |x|) for all x in arr
def softsign(arr):
    for i in range(arr.shape[0]):
        arr[i] = arr[i] / (1 + abs(arr[i]))
    return arr

# assign values from accumulator to the feild.
def make_data():
    
    data = np.array([accu[2][0], accu[2][1], accu[2][2], accu[1][0], accu[1][1], accu[1][2]]);

    return data

# check if the current values of the accu feild are valid.
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

def calc(X):
    W1 = np.array([[  0.3476,  22.0618,  -9.9444,   0.0581,  -0.0805,  -0.0701],
        [  0.1528, -14.7881,   1.9076,  -0.0697,  -0.0030,   0.0716],
        [  0.3600, -20.1983,  -7.4819,  -0.0946,  -0.0941,   0.1036]])

    B1 = np.array([-1.4854, -0.4873, -0.2769])

    W2 = np.array([[ 29.0738,   0.9483, -28.9123]])

    B2 = np.array([-2.0885])

    L1 = softsign(np.add(np.matmul(W1, X), B1))
    Y = softsign(np.add(np.matmul(W2, L1), B2))

    Y = Y[0]

    if Y < LEFT_LIM:
        return LEFT
    elif Y > RIGHT_LIM:
        return RIGHT
    else:
        return STOP


# handler for incoming data
def fallback(path, args, types, src):
    global freq, accu, MODE, COUNT

    if path not in paths.keys():
        # print('error: invalid path: {}'.format(path))
        return
    msg_type = paths[path]

    if msg_type == FORWARD:
        MODE = FRONT
        return
    
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
        
        data = make_data()
        if COUNT == 0:
            MODE = calc(data)
        COUNT += 1
        if COUNT == 10:
            COUNT = 0
        
        accu = copy.deepcopy(Accu)
        freq = copy.deepcopy(Freq)

    return



# add server method to handle data
if __name__ == '__main__':
    server = ''

    # A list of port to connect
    ports = []
    for port in range(5000, 6000, 50):
        ports.append(port)
    
    # Try to establish connection to a port
    connected = False
    for port in ports:
        try:
            server = liblo.Server(port)
            connected = True
            print('Connected to Port {}'.format(port))
            break
        except Error as err:
            print(err)
    
    if not connected:
        print('server not connected')
        sys.exit()

    # add handler to server
    server.add_method(None, None, fallback)

    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    for port in range(1, 100):
        try:
            sock.connect((BOT_ADDR, port))
            print('Connected to {} on port {}'.format(BOT_ADDR, port))
            break
        except bluetooth.btcommon.BluetoothError as e:
            print('{}'.format(e))

    x = 0
    last = -1
    is_moving = 'S'
    try:
        while True:
            if x % 1000000 == 0:
                server.recv(1000)
                if MODE == -1:
                    continue
                if last == command[MODE]:
                    continue;
                last = command[MODE]
                to_send = command[MODE]
                if to_send == 'F':
                    for xt in range(50):
                        sock.send('F')
                sock.send(to_send)
                print(to_send)
            x += 1
    except bluetooth.btcommon.BluetoothError as e:
        print('{}'.format(e))
        sock.close()
