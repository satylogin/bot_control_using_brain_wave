import numpy as np
import math
import copy

def softsign(arr):
	for i in range(arr.shape[0]):
		arr[i] = arr[i] / (1 + abs(arr[i]))
	return arr

cont = ''
with open('front.csv', 'r') as f:
	cont = f.read()
cont = cont.split('\n')

datas = []
for line in cont:
	try:
		data = list(map(float, line.split(',')))
		datas.append(data)
	except ValueError as e:
		print('{}'.format(e))

Y_min = 1e9
Y_max = -1e9

for val in datas:

	X = np.array(val[6:12])

	W1 = np.array([[ -0.7603,  -6.6676,   0.8540,   0.0355,  -0.0095,  -0.0576],
        [  7.5556,  22.6800, -20.0218,  -0.1787,   0.1862,   0.3005],
        [  1.7552, -32.4350,  -4.6349,   0.1049,   0.1786,  -0.1435]])

	B1 = np.array([ 1.3755, -1.3756, -1.1593])

	W2 = np.array([[  1.5355,  28.3488, -29.2707]])

	B2 = np.array([-1.2515])

	# X = input() 6 X 1 [[]]

	L1 = softsign(np.add(np.matmul(W1, X), B1))
	Y = softsign(np.add(np.matmul(W2, L1), B2))
	Y = Y[0]
	Y_min = min(Y_min, Y)
	Y_max = max(Y_max, Y)

print('min: {}, max: {}'.format(Y_min, Y_max))

# eps = 0.33

# if Y < 0 - eps:
# 	MODE = left
# elif Y > 0 + eps:
# 	MODE = right
# else:
# 	MODE = something