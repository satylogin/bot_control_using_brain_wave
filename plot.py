#! /usr/bin/env python

'''
	Code:	 to plot a dynamic graph of the 
		 recieved signals from the neurosky 
		 mindwave. 
	
	Python:  v3 and above

	Author:	 Satyarth Agrahari

	License: Free to edit and distribute
'''

# headers to be imported for plot function to work.
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

lab = ['delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']

# create a figure to plot
fig = plt.figure()

# create a set of graph regions to plot data to
ax = [0 for x in range(8)]
for i in range(8):
	ax[i] = fig.add_subplot(4, 2, i+1)

# create a common x axis data. It will be used for the axis 
# in plot data of all the plots
xs = [i for i in range(5)]

# create empty lists to store the y values of all signals
ys = [[0 for j in range(5)] for i in range(8)]

'''
	This method is used to plot and stimulate a
	dynamic version of graph plotting to give an 
	animated feel (live graph) kind of view
'''
def animate(i):
	# open the file to read the latest data.
	graph_data = open('plot.txt', 'r').read()

	# decompose the files in line.
	lines = graph_data.split('\n')
	
	# traverse each line and get data to be inserted
	# into the graph plot.
	s = ''
	for line in lines:
		if len(line) > 1:
			# get the row and split it using ,
			y = list(line.split(','))
			s = 'Attention: ' + y[0] + ' meditation: ' + y[1]
			for i in range(2, 10):
				# append in the current list and trim the
				# list by one if the length increase more than 5
				ys[i-2].append(y[i])
				if len(ys[i-2]) > 5:
					ys[i-2] = ys[i-2][1:]
	
	# clear the previous plot and then plot the 
	# updated data to give an animated feel
	for i in range(8):
		ax[i].clear()
		ax[i].plot(xs, ys[i])
		ax[i].set_title(lab[i])

'''
	main method to ensure that the function runs only 
	when called from command line
'''
if __name__ == '__main__':
	# begin the animation at an interval of 100 ms
	ani = animation.FuncAnimation(fig, animate, interval = 100)
	plt.show()
