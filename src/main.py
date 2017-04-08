#!/usr/bin/env python3

# Author: Luke Weber
# Creation date: 12/19/2016
# Last modification date: 04/04/2017

"""

[ Project AgiPal ]
    | Learn the skills of developers in attempt to efficiently them assign
    | Sprint tasks, as they are produced by organizations using an Agile
    | development ideology (specifically, SCRUM)

Prior design
Using Passive-Aggressive classifier to learn abstract skills

Proof of Concept design:
    0. Grab GitHub repository (e.g. Bitcoin Core)
    1. Parse all files in repo into standard data structure
    2. Training: Feed 1/2 data to train
    3. Testing: Feed 1/2 data to test
    4. Print results
"""

import sys

import extract as ex  	# Local git repo data extracter
import fetch as fc    	# Web-based git repo extracter
import model as mod    	# Recommender model

def main():

    repo_name = "bitcoin"

    # Extract data from local repo
    print("Extracting data from", repo_name)

    # Mine VCS, up the recursion limit for pickling the pools
    old_limit = sys.getrecursionlimit()
    new_limit = 6000
    sys.setrecursionlimit(new_limit)
    epool, fpool = ex.extract(repo_name, live = False)
    sys.setrecursionlimit(old_limit)
    print("VCS Successfully mined!")

    # See entities attributed to each file
    for fname, fobj in fpool.pool.items():

        print(fname)
        ent_dict = {}

        # Count-up frequency of contributions to this file by each entity
        for ea_id in [ea.entity.id for ea in fobj.eas][:]:
            ent_dict[ea_id] = ent_dict.get(ea_id, 0) + 1

        # Sort by frequency
        ent_list = sorted(list(ent_dict.items()), key = lambda x: -x[1])

        # Display said info, getting only top 5 entities
        for ent, freq in ent_list[:5]:
            print("\t", "({})".format(freq), ent)


def todo_something():
    """ The leftover code from previous assignment """

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
        task_name = input("Task name> ")
        print('"' + task_name + '"')
        task_features = []
        for f in range(len(feature_labels)):
            task_features.append(int(input("[{0}] {1}> ".format(f, feature_labels[f]))))
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
        best_p = int(input("Correct person (0-{0})> ".format(len(people_labels) - 1)))
        print("Okay, so {0} is the best for this task. Thanks!".format(people_labels[best_p]))
        y = [best_p]

        # Update model with our 1 sample
        pac.partial_fit(X, y, range(len(people_labels)))

        n_runs += 1
        print
        if input("Continue (y/n)?> ") == "n": break

    print("=" * 50)

# Drive!
main()
