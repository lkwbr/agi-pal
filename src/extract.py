# extract.py

import os
import queue
import subprocess

def extract(repo_name):
    """ Extract sets X and Y from git repository under the folder '/data' """
   
    # TODO: Remove the hard-coding
    data_dir = "../../Repos"
    os.chdir(data_dir) 
    repo_dir = repo_name 

    # Gather all directory (and subdirectory) files,
    # and then parse them for features 
    file_names = walk_dir(repo_dir)
    X, Y = parse_features(file_names)

    return X, Y 

def parse_features(file_names):
    """ """

    X = []
    Y = []

    for file_name in file_names:

        print(file_name)

        git_cmd = "git log --format=format:%an " + file_name + " | sort | uniq"

        output = subprocess.getoutput(git_cmd)
        print(output)

    return X, Y

def walk_dir(dir_name):
    """
    Iteratively explore and extract data w/in directory structure.
    NOTE: Pervious recursive approach killed stack.
    """

    print(dir_name)

    dir_queue = queue.Queue()
    file_bag = []

    # Walk over current directory
    dir_queue.put(dir_name)
    while not dir_queue.empty():

        curr_dir = dir_queue.get()

        for (dir_path, sub_dir_names, file_names) in os.walk(curr_dir):

            # Add each subdirectory to queue to visit later
            for sub_dir_name in sub_dir_names:  
                dir_queue.put(dir_concat(dir_path, sub_dir_name))

            # Put those filenames in the bag! Adding directory structure
            # to name as well
            file_bag.extend([dir_concat(dir_path, x) for x in file_names])

        print("Scanned directory '" + curr_dir + "'.")

    return file_bag

def dir_concat(dir_pre, dir_post):
    return dir_pre + "/" + dir_post

