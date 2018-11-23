import csv
import random
import math
import src.train as train

def main():
	filename = 'data/sonar.all-data.csv'
	dataset = train.load_csv(filename)

#Convert string to float
	for i in range(0,len(dataset[0]) - 1):
		a = train.str_column_to_float(dataset,i)

#Convert class column to integers
	b = train.str_column_to_integer(dataset, len(dataset[0]) -1 )
	print(b)

main()