# extract.py

import os
import subprocess

def extract(repo_name):
	""" Extract sets X and Y from git repository under the folder '/data' """

	data_dir = "data/"
	cmd = "git shortlog -s -n"

	#os.chdir("C:\Users\DhruvOhri\Documents\COMP 6411\pygithub3-0.3")
	#os.system("git clone https://github.com/poise/python.git")

	os.chdir(data_dir + "repo_name")
	output = subprocess.getoutput(cmd)

	print(output)

	input("Press enter to continue")

	return [], []
