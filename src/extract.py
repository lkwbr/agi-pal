# extract.py

import os
import queue
import subprocess

def extract(repo_name):
	""" Extract sets X and Y from git repository under the folder '/data' """
	
	data_dir = "data/"
	repo_dir = data_dir + repo_name
	cmd = "git shortlog -s -n"

	# Go to data location	
	#os.chdir(repo_dir)

	# Walk through whole directory structure
	file_names = walk_dir(repo_dir)
	
	print(len(file_names))

	output = subprocess.getoutput(cmd)

	print(output)

	return [], []

	# NOTE: May be useful later
	#os.chdir("C:\Users\DhruvOhri\Documents\COMP 6411\pygithub3-0.3")
	#os.system("git clone https://github.com/poise/python.git")

def walk_dir(dir_name):
	"""
	Iteratively explore and extract data w/in directory structure. 
	NOTE: Pervious recursive approach killed stack. 
	"""

	#cmd_two = "git log --format=format:%an " + data_dir + " ver1..ver2 | sort | uniq"

	dir_queue = queue.Queue() 
	file_bag = []

	# Walk over current directory
	dir_queue.put(dir_name)
	while not dir_queue.empty():

		curr_dir = dir_queue.get()

		for (dir_path, sub_dir_names, file_names) in os.walk(curr_dir):
		
			# Add each subdirectory	to queue to visit later
			for sub_dir_name in sub_dir_names: dir_queue.put(sub_dir_name)	

			# Put those filenames in the bag!
			file_bag.extend(file_names)

		break
