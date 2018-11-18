import csv
import random
import math
import src.train as train

def main():
	filename = 'data/sonar.all-data.csv'
	dataset = train.load_csv(filename)
	print (dataset)
main()