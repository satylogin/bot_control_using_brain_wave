from random import shuffle
import pprint

LEFT = 'normalise_data_left.csv'
RIGHT = 'normalise_data_right.csv'
NORMAL = 'normalise_data_front.csv'
MERGE = 'merge.csv'

data = []
pdata = []

def read_data(file_name, label):
	print('File name: ', file_name)
	cont = ''
	with open(file_name, 'r') as f:
		cont = f.read()
	
	cont = cont.split('\n')
	for line in cont:
		if len(line) > 0:
			s = line + ', ' + label
			x = list(map(float, s.split(',')))
			data.append(x)

if __name__ == '__main__':
	read_data(LEFT, '1')
	read_data(RIGHT, '2')
	read_data(NORMAL, '0')

	shuffle(data)

	for x in data:
		s = str(x[0])
		for j in range(1, len(x)):
			s = s + ', ' + str(x[j])
		pdata.append(s) 

	with open(MERGE, 'w') as f:
		for line in pdata:
			f.write(line)
			f.write('\n')
