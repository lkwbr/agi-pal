# extract.py

import os
import subprocess

def extract(repo_name):
	""" Extract sets X and Y from git repository under the folder '/data' """
	
	data_dir = "data/"
	repo_dir = data_dir + repo_name
	cmd = "git shortlog -s -n"

	# Go to data location	
	#os.chdir(repo_dir)

	# Walk through whole directory structure
	file_names = []
	walk_dir(repo_dir, file_names)
	
	print(file_names)

	output = subprocess.getoutput(cmd)

	print(output)

	return [], []

	# NOTE: May be useful later
	#os.chdir("C:\Users\DhruvOhri\Documents\COMP 6411\pygithub3-0.3")
	#os.system("git clone https://github.com/poise/python.git")

def walk_dir(dir_name, file_bag = []):
	"""
	Recursively explore and extract data w/in directory structure. 
	NOTE: We'll have problems if directory contents are of a length
	      such that we run out of our allocated space on stack.
	"""

	#cmd_two = "git log --format=format:%an " + data_dir + " ver1..ver2 | sort | uniq"

	# Walk over current directory
	for (dir_path, sub_dir_names, file_names) in os.walk(dir_name):
	
		# Recurse on each subdirectory	
		for sub_dir_name in sub_dir_names: walk_dir(sub_dir_name, file_bag)	

		# Put those filenames in the bag!
		file_bag.extend(file_names)

