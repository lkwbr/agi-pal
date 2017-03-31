# extract.py

import re
import os
import queue
import subprocess

def extract(repo_name):
    """ Extract sets X and Y from git repository under the folder '/data' """

    # NOTE: For each source file delta, all relevant developers and
    # organizations gain an EA for a particular file, technology, module,
    # subcomponent, etc.

    # TODO: Remove the hard-coding
    data_dir = "../../Repos"
    repo_dir = data_dir + "/" + repo_name
    os.chdir(repo_dir)

    # Gather all directory (and subdirectory) files,
    # and then parse them for features
    file_names = walk_dir(".")
    print("Donesldfkjsdlkfjsdklfj")
    for f in file_names: print(f)
    X, Y = parse_features(file_names)

    return X, Y

def parse_features(file_names):
    """ """

    X = []
    Y = []

    # For each file (key), store the list of its contributors (value)
    file_contributor_dict = {}

    for file_name in file_names:
        parse_git_commit_log(file_name)
        
    print(file_contributor_dict)
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

def parse_git_user_line(l):
    """ 
    Parse given git commit line by single user. e.g., a line could be 
    "Wladimir J. van der Laan    laanwj@gmail.com    Mon Nov 2 04:15:58 2015 +0100",
    which is of the form [name]\t[email]\t[commit datetime]
    """
    
    fields = l.split("\t")
    name = fields[0] 
    email = fields[1] 
    datetime = fields[2] 

    #entity = Entity
    entity

    # TODO: Convert datetime into Pythonic form

def parse_git_numstat_line(l):
    """ 
    Parse given git numstat line, of following form:
    [num inserted lines]\t[num deleted lines]\t[relative filename] 
    """

    fields = l.split("\t")

def parse_git_commit_log(f):
    """ Parse given file's git commit log """

    # Get developer name, email, datetime, number of inserted lines, 
    # and the number of deleted lines
    # NOTE: Potential loss of information by ignoring merges! Only taking not
    # of changes to master branch
    commit_format = "%an'\t'%ae'\t'%ad'\t'"
    git_commits = ("git log --format={} --no-merges --numstat {} | sed '/^$/d'") \
            .format(commit_format, f)
    output = subprocess.getoutput(git_commits)
    lines = output.split('\n')

    # Partition commits
    pattern = re.compile("^[0-9]\t[0-9]\t[A-Z]+.[A-Z]+$", re.IGNORECASE)
    # TODO: Do that list comprehension pairing thing again!
    for l in lines:
        print(l)
        if pattern.match(l): delta_stats = parse_git_numstat_line(l)
        else: delta_entity = parse_git_user_line(l)

    exit(0)

    #delta = Delta(f, )

    #contributors = output.split("\n")
    file_contributor_dict[f] = contributors
