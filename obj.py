#!/usr/bin/env python3

# Luke Weber, 11398889
# Created 12/19/16

"""
Using Passive-Aggressive classifier to learn abstract skills
"""

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
