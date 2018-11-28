from random import seed
from random import randrange
from csv import reader
from math import sqrt
from rf_testing import *

def main():
	# Make a prediction with a list of bagged trees
	def bagging_predict(trees, row):
		predictions = [predict(tree, row) for tree in trees]
		return max(set(predictions), key=predictions.count)

	# Random Forest Algorithm
	def random_forest(train, test, max_depth, min_size, sample_size, n_trees, n_features):
		trees = list()
		for i in range(n_trees):
			sample = subsample(train, sample_size)
			tree = build_tree(sample, max_depth, min_size, n_features)
			trees.append(tree)
		predictions = [bagging_predict(trees, row) for row in test]
		return(predictions)

	# Test the random forest algorithm
	seed(2)
	# load and prepare data
	filename = 'data/dt_test.csv'
	dataset = load_csv(filename)
	# convert string attributes to integers
	for i in range(0, len(dataset[0])-1):
		str_column_to_float(dataset, i)
	# convert class column to integers
	str_column_to_int(dataset, len(dataset[0])-1)
	# evaluate algorithm
	n_folds = 5
	max_depth = 10
	min_size = 1
	sample_size = 1.0
	n_features = int(sqrt(len(dataset[0])-1))
	for n_trees in [10, 25, 50]:
		scores = evaluate_algorithm(dataset, random_forest, n_folds, max_depth, min_size, sample_size, n_trees, n_features)
		print('Trees: %d' % n_trees)
		print('Scores: %s' % scores)
		print('Mean Accuracy: %.3f%%' % (sum(scores)/float(len(scores))))

main()
