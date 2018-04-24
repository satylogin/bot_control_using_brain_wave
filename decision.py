import time
import bluetooth
import numpy as np
import math


def sigmoid(arr):
	for i in range(arr.shape[0]):
		arr[i][0] = (1 / (1 + math.exp(-1.0 * arr[i][0])))		


wij = np.zeros((8, 5), dtype = float)
wjk = np.zeros((5, 2), dtype = float)
bz = np.zeros((5, 1), dtype = float)
wij = np.zeros((2, 1), dtype = float)


wij = np.array([[  4.43429875, -12.52808526,   4.43429875, -12.52808526,   5.25333943],
 [  0.03745447,   2.3358748,    0.03745447,   2.3358748,   -6.25915743],
 [ -5.70691156,   0.41894822,  -5.70691156,   0.41894822,  -7.82465262],
 [-10.3614143,   -4.5465339,  -10.3614143,   -4.5465339,  -15.09470312],
 [  5.05946983,  -5.61912148,   5.05946983,  -5.61912148,  -5.70553943],
 [ -8.15445716,  -3.82457571,  -8.15445716,  -3.82457571,  -6.00744297],
 [ -8.64499405,  -4.78760607,  -8.64499405,  -4.78760607,  -5.56306821],
 [ -1.81195006,  -6.18049982,  -1.81195006,  -6.18049982,  -1.69009039]])
 
wjk = np.array([[ 1.96652458, -1.96652458],
 [ 2.8073538,  -2.8073538 ],
 [ 1.96652458, -1.96652458],
 [ 2.8073538,  -2.8073538 ],
 [ 4.97999987, -4.97999987]])

bz = np.array([[-5.65865195],
 [-1.886964  ],
 [-5.65865195],
 [-1.886964  ],
 [ 1.48620896]])

by = np.array([[-3.98797795],
 [ 3.98797795]])


x = np.zeros((8, 1), dtype = float)
z = np.zeros((5, 1), dtype = float)
y = np.zeros((2, 1), dtype = float)


mn = [774501.4106583073, 235672.6802507837, 68508.85579937304, 49190.5078369906, 43842.41379310345, 39930.645768025075, 26266.96238244514, 16355.510971786834, 0.4043887147335423]

sd = [423714.54677880264, 179275.45217596702, 74286.10460040563, 49912.85190712203, 43352.12456537028, 40811.21212921624, 26302.60738573058, 21955.374204181397, 0.4915444015957941]


start = 0

while(1):

	data = list(map(float, (((open('plot.txt', 'r').read()).split('\n'))[0]).split(',')))
	focus = data[0];
	data = data[2:]
	for i in range(8):
		data[i] = (data[i] - mn[i]) / sd[i]
	x = np.array(data)
	x = x.reshape((8, 1))


	z = np.add(np.transpose(np.matmul(np.transpose(x), wij)), bz)
	sigmoid(z)
	y = np.add(np.transpose(np.matmul(np.transpose(z), wjk)), by)
	sigmoid(y)

	fd = open('command.txt', 'w')
	if focus >= 55:
		start = 1
	elif focus <= 40:
		start = 0

	if start == 0:
		fd.write("S");
	elif y[0][0] > y[1][0]:
		fd.write("F")
		print("0")
	else:
		fd.write("L")
		print("1")
	time.sleep(1)
