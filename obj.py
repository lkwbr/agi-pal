# Luke Weber, 11398889
# CptS 570, Course Project
# Created 12/19/16

"""
Contains both project init code and objective function used by Spearmint

Using Bayesian optimization library (Spearmint) on SVM classifier (LibSVM)
for automated hyper-parameter tuning!
"""

# Imports
import sys
sys.path.append("libsvm/libsvm-3.21/python")
from svmutil import *
from parse import *

# ----------------------------------------------------------

from sklearn.linear_model import PassiveAggressiveClassifier 
import numpy as np

def main():
	# Model and params
	pac = PassiveAggressiveClassifier()
	n_samples = 1 # at a time
	feature_labels = ["Software development", "Web development", "IT", "Social", "Tester"]
	people_labels = ["Jessica", "Ron", "Patricia", "Qu"]	

	# Organization info
	print("=" * 50)
	print("ORGANIZATION INFO")
	print("Population: {0}".format(str(people_labels)))
	print("Performance metrics: {0}".format(str(feature_labels)))
	print

	# Train
	n_runs = 0
	while True:
		# Header
		print("-" * 50)

		# Get task name and features
		print("TASK BREAKDOWN")
		task_name = raw_input("Task name> ")
		print('"' + task_name + '"')
		task_features = []
		for f in range(len(feature_labels)):
			task_features.append(int(raw_input("[{0}] {1}> ".format(f, feature_labels[f]))))
		X = [task_features] #np.zeros((n_samples, len(feature_labels)))

		# Predict best person for task
		if n_runs > 0:
			print
			print("PREDICT PERSON")
			pred_p = pac.predict(X)[0]
			print("Predicted person: {0}".format(people_labels[pred_p]))

		# Get actual best
		print
		print("CORRECT PERSON")
		best_p = int(raw_input("Correct person (0-{0})> ".format(len(people_labels) - 1)))
		print("Okay, so {0} is the best for this task. Thanks!".format(people_labels[best_p]))
		y = [best_p]	
	
		# Update model with our 1 sample 
		pac.partial_fit(X, y, range(len(people_labels))) 


		n_runs += 1
		print
		if raw_input("Continue (y/n)?> ") == "n": break

	print("=" * 50)

# Drive!
main()

# ----------------------------------------------------------

# Globals
prob = None
validation_labels = None
validation_data = None
train_labels = None
train_data = None

def init():
	"""
	Train SVM on only first fold of Optical Character Recognition (OCR) data
	"""
	
	# Parse train data: [80%] train.txt, [20%] validation.txt
	global prob, validation_labels, validation_data, train_labels, train_data

	parse_input("data/ocr_fold0_sm_train.txt")
	train_labels, train_data = svm_read_problem("train.txt")
	validation_labels, validation_data = svm_read_problem("validation.txt")

	# Formulate SVM problem
    	prob = svm_problem(train_labels, train_data)

def main_past(job_id, params):
	"""
	Objective function called by Spearmint to determine desirability of 
	the parameters C and gamma:
		- Setup params
		- Train SVM, get model
		- Test SVM
		- Return accuracy
	"""

	# Setup
	init()

	# Set SVM params; NOTE: "-q" silences training output
	c = params["c"][0]
	g = params["g"][0]
	
	param = svm_parameter("-c {0} -g {1} -q".format(c, g))
	print("[JOB{0}] Training with c = {1:.3f}, g = {2:.3f}...".format(job_id, c, g))	

	# Train model
	m = svm_train(prob, param)

	# Predict
	pred_lbl, pred_acc, pred_val = svm_predict(validation_labels, validation_data, m)

	# Parse and return accuracy - inverse it so that
	# minimizing this function will maximize our accuracy
	acc = pred_acc[0]
	print("[LUKE_TOKEN] Accuracy = {0}".format(acc))	
	inv_acc = 100 - acc
	
	return inv_acc 
