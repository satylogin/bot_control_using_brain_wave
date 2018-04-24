import numpy as np
import pandas as pd
import math
import csv

def softmax(arr):
	den = 0.0

	for i in range(arr.shape[0]):
		den += math.exp(arr[i][0])

	for i in range(arr.shape[0]):
		num = math.exp(arr[i][0])
		arr[i][0] = (num / den)

	return


def sigmoid(arr):
	for i in range(arr.shape[0]):
		#try:
                arr[i][0] = (1 / (1 + math.exp(-1.0 * arr[i][0])))		
		#except OverflowError:
			#arr[i][0] = float('inf')


def normalize(x_train):
	for j in range(x_train.shape[1]):
		s = 0.0
		for i in range(x_train.shape[0]):
		        s += x_train[i][j]

		mean = s / x_train.shape[0]
		ersq = 0.0

		for i in range(x_train.shape[0]):
		        ersq += (x_train[i][j] - mean) ** 2

		sd = (ersq / (x_train.shape[0] - 1)) ** 0.5

		for i in range(x_train.shape[0]):
		        x_train[i][j] = (x_train[i][j] - mean) / sd

	return
		


l1 = 8
l2 = 5
l3 = 2


df = pd.read_csv("data_satyarth.csv")
data = df.as_matrix()

normalize(data)


x = np.zeros((l1, 1), dtype = float)
z = np.zeros((l2, 1), dtype = float)
y = np.zeros((l3, 1), dtype = float)

y_train = np.zeros((l3, 1), dtype = float)

wij = np.zeros((l1, l2), dtype = float)
wjk = np.zeros((l2, l3), dtype = float)

dwij = np.zeros((l1, l2), dtype = float)
dwjk = np.zeros((l2, l3), dtype = float)

bz = np.zeros((l2, 1), dtype = float)
by = np.zeros((l3, 1), dtype = float)


curr = 0.001

for i in range(wij.shape[0]):
	for j in range(wij.shape[1]):
		wij[i][j] = curr
		curr *= -1.0

for j in range(wjk.shape[0]):
	for k in range(wjk.shape[1]):
		wjk[j][k] = curr
		curr *= -1.0

for i in range(bz.shape[0]):
	bz[i][0] = curr
	curr *= -1.0

for i in range(by.shape[0]):
	by[i][0] = curr
	curr *= -1.0


epochs = 10000
alpha = 0.12
beta = 0.95


"""
print(wij)
print(wjk)
"""


for l in range(epochs):

	mse = 0.0

	for k in range(data.shape[0]):

		x = data[k][2:10]
		x = x.reshape((8, 1))
		#print(x.shape)

		if(data[k][10] == 0):
			y_train = [[1.0], [0.0]]
		else:
			y_train = [[0.0], [1.0]]


		dk = np.zeros((l3, 1), dtype = float)
		dj = np.zeros((l2, 1), dtype = float)

		z = np.add(np.transpose(np.matmul(np.transpose(x), wij)), bz)

		sigmoid(z)

		y = np.add(np.transpose(np.matmul(np.transpose(z), wjk)), by)

		sigmoid(y)


		mse += ((y[0][0] - y_train[0][0]) ** 2 + (y[1][0] - y_train[1][0]) ** 2) / 2

		for i in range(dk.shape[0]):
			dk[i][0] = y[i][0] * (1 - y[i][0]) * (y_train[i][0] - y[i][0])

		for j in range(wjk.shape[0]):
			for k in range(wjk.shape[1]):
				temp = alpha * z[j][0] * dk[k][0] + beta * dwjk[j][k]
				wjk[j][k] += temp
				dwjk[j][k] = temp
				

		for k in range(by.shape[0]):
			by[k][0] += alpha * dk[k][0] 

		for j in range(dj.shape[0]):
			for k in range(dk.shape[0]):
				dj[j][0] += z[j][0] * (1 - z[j][0]) * dk[k][0] * wjk[j][k]

		for j in range(bz.shape[0]):
			bz[j][0] += alpha * dj[j][0]

		for i in range(wij.shape[0]):
			for j in range(wij.shape[1]):				
				temp = alpha * x[i][0] * dj[j][0] + beta * dwij[i][j]
				wij[i][j] += temp
				dwij[i][j] = temp

	if(l % 10 == 0):
		alpha *= 0.996
		mse = (mse / (data.shape[0] - 1)) ** 0.5
		print(mse)


print(wij)
print(wjk)
print(bz)
print(by)
