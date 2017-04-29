# mine.py

import re
import os
import time
import queue
import pickle
import subprocess
from datetime import datetime

# Personal classes
from xp import *
from util import *
from entity import *

class RepoMiner:
    """ Experience miner for any given code base using Git VCS """

    __name__ = "Git Repository Experience Miner"
    base_repo_dir = "../../Repos/"

    def __init__(self, repo_name):

        print("Repository Miner created!")

        # Get bearings
        self._repo_name = repo_name
        self._repo_dir = self.base_repo_dir + self._repo_name
        self._project_dir = os.getcwd()

        # Update repo
        self._update()

    def _load(self, arg):
        """ Load given class name, raising exception if not previously pickled """

        # Check if file exists to begin with
        pickle_dir = self._project_dir + "/pickle/"
        fname = pickle_dir + arg + ".pickle"
        if not os.path.exists(fname): raise ValueError

        # Load pickled file as data!
        pickle_file = open(fname, "rb")
        data = pickle._load(pickle_file)
        pickle_file.close()
        return data

    def _save(self, *args):
        """ Picklize all given classes """

        print("Saving [{}] via pickle".format(", ".join(args)))

        # Attempt to serialize our classes (and thus, our data) with pickle
        # NOTE: Must open the files in binary mode ("b")
        pickle_dir = self._project_dir + "/pickle/"
        for a in args:
            with open("{}{}.pickle".format(pickle_dir, a.__name__), "wb+") as f:
                pickle.dump(a, f)

        print("...Saved")

    def mine(self, live = True, keep = True):
        """ Extract repository data into custom objects """

        # NOTE: For each source file delta, all relevant developers and
        # organizations gain an EA for a particular file, technology, module,
        # subcomponent, etc.
        # NOTE: Expecting all (git) repos to be in a folder at "../../Repos/"

        print("Extracting data from {}".format(self._repo_name))
        epool, fpool = (None, None)

        # We have choice to do new extraction, or to load a previous one
        if not live:

            # Load collection of entities and files
            epool = self._load("EntityPool")
            fpool = self._load("FilePool")

        else:

            # Change to code base directory (for git functionality), while also
            # storing the source directory
            os.chdir(self._repo_dir)

            # Gather all directory (and subdirectory) files, and then parse them
            # into the proper classes
            print("Scanning {} code base".format(self._repo_name))
            file_names = self._walk_dir(".")
            print("...Collected {} source code files".format( \
                len(file_names), self._repo_dir))
            epool, fpool = self._parse_git_logs(file_names)

            # Come back to the project, my love!
            os.chdir(self._project_dir)

            # Save the pools
            if keep: self._save(epool, fpool)

        print("...Data extracted!")
        return epool, fpool

    def _update(self):
        """ Update given repository to most recent state """

        print("Updating repository: {}".format(self._repo_name))

        # Change directory to repository
        os.chdir(self._repo_dir)

        # Update repo with git
        git_cmd = ("git pull")
        output = subprocess.getoutput(git_cmd)

        # Move back
        os.chdir(self._project_dir)

        print("...Up to date")
        return self

    @staticmethod
    def _parse_git_logs(file_names):
        """ Parse git change/commit logs from argument list of file names """

        # Initialize our object pools
        epool = EntityPool()
        fpool = FilePool()

        # Vars for remaining time estimation
        i = 0
        t = 0
        l = len(file_names)
        s = sum([y for x, y in file_names])
        start_time = time.time()

        print()
        for file_name, file_len in file_names[:]:

            i += 1
            t += file_len

            # Parse stuff
            RepoMiner._parse_git_commit_log(file_name, epool, fpool)

            # Prediction stuff
            elapsed = time.time() - start_time      # s
            avg_time_per_mb = elapsed / t           # s
            remaining_mb = s - t

            time_left = remaining_mb * avg_time_per_mb
            time_left_min = round((time_left / 60), 2)

            # Display stuff
            restart_line()
            time_left_str = "{} {}".format(time_left_min, "minutes left")
            sys.stdout.write("[{}/{}] {} {}".format(i, l, time_left_str, file_name))
            sys.stdout.flush()

        # Print iteration info
        print()
        print()
        for eid, e in epool.pool.items(): print("\t", len(e.eas), "\t", eid)
        print()
        print("-" * 30)
        print(len(epool.pool), "developers")
        print(len(fpool.pool), "files")
        print("-" * 30)
        print()

        return epool, fpool

    @staticmethod
    def _walk_dir(dir_name):
        """
        Iteratively explore and extract data w/in whole directory structure
        NOTE: Pervious recursive approach killed stack, so we expanded stack size
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
                    dir_queue.put(RepoMiner._dir_concat(dir_path, sub_dir_name))

                # Put those filenames in the bag! Adding directory structure
                # and file size to name as well
                curr_dir_files = [
                    (RepoMiner._dir_concat(dir_path, x), \
                    os.stat(RepoMiner._dir_concat(dir_path, x)).st_size) \
                    for x in file_names]
                file_bag.extend(curr_dir_files)

        return file_bag

    @staticmethod
    def _dir_concat(dir_pre, dir_post):
        return dir_pre + "/" + dir_post

    @staticmethod
    def _parse_and_package(f, l):
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

    @staticmethod
    def _create_delta(data):
        """ Simple. From data, create Delta object """

        delta = Delta(
            data["abs_file"],
            data["num_insert"],
            data["num_delete"],
            data["date_time"])

        return delta

    @staticmethod
    def _get_entities(data, epool):
        """ Get Entity objects from single delta, making sure they're in the pool """

        # TODO: Add organizational entities

        # Parse entities associated with this single delta
        name = data["name"]
        email = data["email"]

        # Get/create entity
        entity = epool.get(email)
        if entity is None:
            # Add new entity to the entity pool
            entity = Entity(name, email)
            epool.add(entity)

        return [entity]

    @staticmethod
    def _parse_git_commit_log(f, epool, fpool):
        """ Parse given file's git commit log """

        # NOTE: Potential loss of information by ignoring merges! Only taking not
        # of changes to master branch

        # Get developer name, email, datetime, number of inserted lines,
        # and the number of deleted lines
        pretty_format = "\"%an\t%ae\t%ad\t\""
        git_commits = ("git log --format={} --no-merges --numstat {} | sed \"/^$/d\"") \
            .format(pretty_format, f)
        output = subprocess.getoutput(git_commits)
        lines = output.split('\n')

        # Instantiate file object from file path and add to file pool
        ffile = File(f)
        fpool.add(ffile)

        # Pair each commit author with commit stats
        pairs = [x + y for x, y in zip(lines[::2], lines[1::2])]
        for p in pairs:

            # Parse commit info
            data = RepoMiner._parse_and_package(f, p)

            # Create delta from data
            delta = RepoMiner._create_delta(data)

            # Gather list of entities relevant to delta:
            # developers, organizations, etc.
            entities = RepoMiner._get_entities(data, epool)

            # Link each entity from delta to a unique EA, which is then linked
            # to the (argument) file
            for entity in entities:

                # Birth of new EA for this entity
                ea = ExperienceAtom(entity, ffile, delta)

                # Double-sided link, where EA is middle of link
                ffile.link(ea)
                entity.link(ea)
