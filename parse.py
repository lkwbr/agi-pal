# Original author: Shyam Gopal
# Editor: Luke Weber 
# Last changed on 12/17/16

"""
Parses and formats the OCR data to 80% sub-train and
20% validation data, all to be processed by LibSVM
"""

import os.path

def create_feature_string(features):
	features = features[2:]
	feat_str = ""
	for index in range(len(features)):
		feat_str += str(index + 1) + ':' + str(features[index]) + ' '
	return feat_str

def parse_input(input_file):
        train_output_file = "train.txt"
        validation_output_file = "validation.txt"
        
	lines = list()
	with open(input_file, 'r') as tf:
		lines = tf.readlines()
	
	train_length = int(len(lines) * 0.8)

        # Train data (80%)
	if not os.path.isfile(train_output_file):
		with open(train_output_file, 'w+') as tof:
			for line in lines[:train_length]:
				if (len(line) < 5):
					continue
				line_split = line.strip().split('\t')
				features = line_split[1]
				label = ord(line_split[2]) - ord('a')
				feature_string = create_feature_string(features)
				output_line = str(label) + " " + feature_string + "\n"
				tof.write(output_line)

        # Validation data (20%)
	if not os.path.isfile(validation_output_file):
		with open(validation_output_file, 'w+') as tof:
			for line in lines[train_length:]:
				if (len(line) < 5):
					continue
				line_split = line.strip().split('\t')
				features = line_split[1]
				label = ord(line_split[2]) - ord('a')
				feature_string = create_feature_string(features)
				output_line = str(label) + " " + feature_string + "\n"
				tof.write(output_line)

	# Fin!
	print("Done parsing train and validation data!")
