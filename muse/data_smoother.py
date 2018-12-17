#!/usr/bin/env python

import csv
import math

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

INPUT_FILE = 'muse_eeg_data.csv'
OUTPUT_FILE = 'normalise_data.csv'
NORMALISE_FACTOR = 3

if __name__ == '__main__':
	data = {}

	for field in fieldnames:
		data[field] = 0 

	with open(OUTPUT_FILE, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
 
		with open(INPUT_FILE, 'r') as csvfile:
			reader = csv.DictReader(csvfile, fieldnames=fieldnames)
			next(reader, None)
			count = 0
			for row in reader:
				count += 1
				for key in row.keys():
					data[key] += float(row[key])
				if count == NORMALISE_FACTOR:
					for key in data.keys():
						data[key] /= count
					writer.writerow(data)
					for key in data.keys():
						data[key] = 0
					count = 0
		
		print('File write complete')
    	