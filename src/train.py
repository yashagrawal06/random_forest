#Importing the libraries
from random import seed
from random import randrange
from csv import reader
from math import sqrt

#Load the CSV file
def load_csv(filename):
	dataset = list()
	with open(filename,  "r") as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset


#Convert string column to float
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())

#Convert string column to integer
def str_column_to_int(dataset, column):
	class_values = [row[column] for row in dataset]
	unique = set(class_values)
	lookup = dict()
	for i, value in enumerate(unique):
		lookup[value] = i
	for row in dataset:
		row[column] = lookup[row[column]]
	return lookup

#Cross-Validation
def cross_validation_split(dataset,k_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset)/k_folds)
	for i in range(k_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split

#Calculate accuracy
def metric_accuracy(actual, predicted):
	correct_pred = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct_pred +=1
	return correct_pred / float(len(actual)) * 100.0

#Split dataset based on attribute and attribute value
def test_split(index, value, dataset):
	left, right = list(), list()
	for row in dataset:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	return left, right



#Evaluate algorith with cross_validation_split
def evaluate_algorithm(dataset, algorithm, k_folds, *args):
	folds = cross_validation_split(dataset, k_folds)
	scores = list()
	for fold in folds:
		train_set = list(folds)
		train_set.remove(fold)
		train_set = sum(train_set, [])
		test_set = list()
		for row in fold:
			row_copy = list(row)
			test_set.append(row_copy)
			row_copy[-1] = None
		predicted = algorithm(train_set, test_set, *args)
		actual = [row[-1] for row in fold]
		accuracy = metric_accuracy(actual, predicted)
		scores.append(accuracy)
	return scores

#Calculate Gini Index for Split
def gini_index(groups, class_values):
	gini = 0.0
	for class_value in class_values:
		for group in groups:
			size = len(group)
			if size ==0:
				continue
			proportion = [row[-1] for row in group].count(class_value)
			float(size)
			gini += (proportion * (1.0-proportion))
	return gini

#Select best split point for dataset
def get_split(dataset, n_features):
	class_values = list(row[-1] for row in dataset)
	b_index, b_value, b_score, b_groups = 999, 999, 999, None
	features = list()
	while len(features) < n_features:
		index = randrange(len(dataset[0])-1)
		if index not in features:
			features.append(index)
	for index in features:
		for row in dataset:
			groups = test_split(index, row[index], dataset)
			gini = gini_index(groups, class_values)
			if gini < b_score:
				b_index, b_value, b_score, b_groups = index, row[index], gini,  groups
	return{'index': b_index, 'value':b_value, 'groups':b_groups}

#Create a terminal node value
def to_terminal(group):
	outcomes = [row[-1] for row in group]
	return max(set(outcomes), key=outcomes.count)

#Create Child Splits or terminal/leaf node
def split(node, max_depth, min_size, n_features, depth):
	left, right = node['groups']
	del(node['groups'])
	if not left or not right:
		node['left'] = node['right'] = to_terminal(left+right)
		return
	if depth >= max_depth:
		node['left'], node['right'] = to_terminal(left), to_terminal(right)
		return
	if len(left) <= min_size:
		node['left'] = to_terminal(left)
	else:
		node['left'] = get_split(left, n_features)
		split(node['left'], max_depth, min_size, n_features, depth+1)
	if len(right) <= min_size:
		node['right'] = to_terminal(right)
	else:
		node['right'] = get_split(right, n_features)
		spilt(node['right'], max_depth, min_size, n_features, depth+1)

#Build a Decision Tree
def build_tree(train, max_depth, min_size, n_features):
	root = get_split(train, n_features)
	split(root, max_depth, min_size, n_features, 1)
	return root

def subsample(dataset, ratio):
	sample = list()
	n_sample = round(len(dataset) * ratio)
	while len(sample) < n_sample:
		index = randrange(len(dataset))
		sample.append(dataset[index])
	return sample


#Predictions with Decision Tree
def predict(node, row):
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']
