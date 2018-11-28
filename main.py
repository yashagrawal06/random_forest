from random import seed
from random import randrange
from csv import reader
from math import sqrt
import src.train as train

def main():
	filename = 'data/sonar.all-data.csv'
	dataset = train.load_csv(filename)

#Convert string to float
	for i in range(0,len(dataset[0]) - 1):
		train.str_column_to_float(dataset,i)

#Convert str to int
	train.str_column_to_int(dataset, len(dataset[0])-1)

#Make prediction with list of bagged trees
	def bagging_predictions(trees, row):
		predictions = [predict(tree, row) for tree in trees]
		return max(set(predictions), key=predictions.count)

#Random Forest algorithm
	def random_forest(train, test, max_depth, min_size, sample_size, n_trees,
	n_features):
		trees = list()
		for i in range(n_trees):
			sample = train.subsample(train, sample_size)
			tree = build_tree(sample, max_depth, min_size, n_features)
			trees.append(tree)
		predictions = [bagging_predictions(trees, row) for row in test]
		return(predictions)

#Test the random forest algorithm
	k_folds = 5
	max_depth = 10
	min_size = 1
	sample_size = 1.0
	n_features = int(sqrt(len(dataset[0])-1))
	for n_trees in [1, 5, 10]:
		scores = train.evaluate_algorithm(dataset, random_forest, k_folds,
		max_depth, min_size, sample_size, n_trees, n_features)
		print('Trees: %d' % n_trees)
		print('Scores: %s' % scores)
		print('Mean accuracy: %.3f%%' % (sum(scores)/float(len(scores))))

main()
