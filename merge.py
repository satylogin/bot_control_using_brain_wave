'''
	Code:	to merge to kind of data csv files.
		1. read during the time the subject was blinking
		2. read during the time the subject was not blinking

	Version: python 3.x 

	Author: Satyarth Agrahari

	License: Free to edit and distribute
'''

from random import shuffle

# open the files that contain the record of the
# data from neurosky mindwave
#
# blink will assume that the data contained wha during
# the process when the subject was blinking
#
# normal will assume every other condition

blink = open('saty_blink.csv', 'r').read()
normal = open('saty_normal.csv', 'r').read()

# break the file in lines
lblink = blink.split('\n')
lnormal = normal.split('\n')

num = []
data = []

# since the first file was assumed to be read while 
# the subject was blinking, the value in the blink field
# will be stored as 1
for line in lblink:
	if len(line) > 0:
		s = line + ', 1'
		x = list(map(int, s.split(',')))
		num.append(x)

# we are going to take the running average of 3 samples
# and then going to compute the average value to reduce the
# flickers in the data value and smoothen the reading
i = 0
while i+2 < len(num):
	a = num[i]
	b = num[i+1]
	c = num[i+2]
	for j in range(len(a)):
		a[j] = (a[j] + b[j] + c[j]) // 3
	data.append(a)
	i += 3

num = []


# since the first file was assumed to be read while 
# the subject was not blinking, the value in the blink field
# will be stored as 0
for line in lnormal:
	if len(line) > 0:
		s = line + ', 0'
		x = list(map(int, s.split(',')))
		num.append(x)


# we are going to take the running average of 3 samples
# and then going to compute the average value to reduce the
# flickers in the data value and smoothen the reading
i = 0
while i+2 < len(num):
	a = num[i]
	b = num[i+1]
	c = num[i+2]
	for j in range(len(a)):
		a[j] = (a[j] + b[j] + c[j]) // 3
	data.append(a)
	i += 3

# we are going to shuffle the data to create a more
# random kind of sample
shuffle(data)

# this will be the level field of the csv file, it is going to show the heading of the data vaalues
print('attention, meditation, delta, theta, low-alpha, high-alpha, low-beta, high-beta, low-gamma, mid-gamma, blink')

# this will store the final data value
pdata = []

# convert the list into string to remove undesired [ and ]
for x in data:
	s = str(x[0])
	for j in range(1, len(x)):
		s = s + ', ' + str(x[j])
	pdata.append(s)

# print the data. The output should be redirect in an output file using > on bash
for line in pdata:
	print(line)
