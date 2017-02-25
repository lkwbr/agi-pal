# model.py

from sklearn.linear_model import PassiveAggressiveClassifier
import numpy as np

class RecommenderModel:

    pac = PassiveAggressiveClassifier()
    n_samples = int()
    X = []
    Y = []

    def train(self, X, Y):
        """
        Train model on set of input feature vectors X and set of
        corresponding labels Y.
        """

        pass

    def predict(self, x):
        """
        Give inferred best label y^ for given input features x.
        """

        pass

    def __init__(self, X, Y):

        # If X and Y are not null, train on them when constructor
        # is called.
        if X is not None and Y is not None: train(self, X, Y)
