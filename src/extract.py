# extract.py

import re
import os
import queue
import subprocess
from datetime import datetime

# Personal classes
from entity import *
from experience import *

def extract(repo_name):
    """ Extract sets X and Y from git repository under the folder '/data' """

    # NOTE: For each source file delta, all relevant developers and
    # organizations gain an EA for a particular file, technology, module,
    # subcomponent, etc.

    # TODO: Remove the hard-coding
    # Change to code base directory (for git functionality)
    data_dir = "../../Repos"
    repo_dir = data_dir + "/" + repo_name
    os.chdir(repo_dir)

    # Gather all directory (and subdirectory) files, and then parse them
    # for features
    print("Scanning code base...")
    file_names = walk_dir(".")
    print("Collected {} source code files in {}".format(len(file_names), repo_dir))
    parse_git_logs(file_names)

def parse_git_logs(file_names):
    epool = EntityPool()
    fpool = FilePool()
    for file_name in file_names: parse_git_commit_log(file_name, epool, fpool)

    # Print iteration info
    for eid, e in epool.pool.items():
        print("\t", len(e.ea_list), "\t", eid)
    print()
    print("-" * 30)
    print(len(epool.pool), "developers (so far)")
    print(len(fpool.pool), "files (so far)")
    print("-" * 30)
    print()

def walk_dir(dir_name):
    """
    Iteratively explore and extract data w/in directory structure.
    NOTE: Pervious recursive approach killed stack.
    """

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

        #print("Scanned directory '" + curr_dir + "'.")

    return file_bag

def dir_concat(dir_pre, dir_post):
    return dir_pre + "/" + dir_post

def parse_and_package(f, l):
    """
    Parse given git delta line by single user, i.e., a line of the form
        "[name]\t[email]\t[commit datetime]\t[num inserted lines] \
        \t[num deleted lines]\t[relative filename]"
    Parse and package up all information given!
    """

    # Tokenize for fields
    fields = l.split("\t")

    # Entity-related
    name = fields[0]
    email = fields[1]

    # Delta-related
    abs_file = f
    # Time format example: "Tue Oct 28 21:33:23 2014 -0400"
    date_time = datetime.strptime(fields[2], "%a %b %d %H:%M:%S %Y %z")
    try:
        num_insert = int(fields[3])
        num_delete = int(fields[4])
    except:
        # "git log --numstat ..." will sometimes give hyphens instead of 0s
        num_insert = 0
        num_delete = 0

    # Package-up
    commit_data = {
        "name": name,
        "email": email,
        "abs_file": abs_file,
        "date_time": date_time,
        "num_insert": num_insert,
        "num_delete": num_delete }

    return commit_data

def create_delta(data):
    """ Simple. From data, create Delta object """

    delta = Delta(
        data["abs_file"],
        data["num_insert"],
        data["num_delete"],
        data["date_time"])

    return delta

def get_entities(data, pool):

    # TODO: Add organizational entities

    # Parse entities associated with this single delta
    name = data["name"]
    email = data["email"]
    entity = pool.get(email, name)

    return [entity]

def parse_git_commit_log(f, epool, fpool):
    """ Parse given file's git commit log """

    # NOTE: Potential loss of information by ignoring merges! Only taking not
    # of changes to master branch

    print("Parsing", f)

    # Get developer name, email, datetime, number of inserted lines,
    # and the number of deleted lines
    pretty_format = "\"%an\t%ae\t%ad\t\""
    git_commits = ("git log --format={} --no-merges --numstat {} | sed \"/^$/d\"") \
        .format(pretty_format, f)
    output = subprocess.getoutput(git_commits)
    lines = output.split('\n')

    # Pair each commit author with commit stats
    pairs = [x + y for x, y in zip(lines[::2], lines[1::2])]
    for p in pairs:

        # Parse commit info
        data = parse_and_package(f, p)

        # Create delta from data
        delta = create_delta(data)

        # Gather list of entities relevant to delta:
        #   developers, organizations, etc.
        entities = get_entities(data, epool)
        for e in entities:

            # Birth of new EA for this entity
            ea = ExperienceAtom(e, delta)
            e.add(ea)

            # Add entity (contributor) to file in file pool (if not already there)
            fpool.get(f).add(e)
