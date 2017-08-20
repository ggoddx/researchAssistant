from prepClfData import ClfData
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import (PassiveAggressiveClassifier, Perceptron,
                                  RidgeClassifier, SGDClassifier)
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid

import csv, getSysArgs, results
import numpy as np


def main():
    ## Number of folds for cross-validation
    N_FOLDS = 5

    ## Training data for classification
    train = ClfData(getSysArgs.usage(['msgTypeClf_xval.py',
                                      '<train_data_filepath>',
                                      '<observation_column_name>',
                                      '<label_column_name>'])[1:])

    train.randomize()

    ## Text vectorizer
#    txt2vect = CountVectorizer(binary = True, ngram_range = (1, 2),
#                               max_df = 0.45)#, min_df = 0.01)
    txt2vect = TfidfVectorizer(max_df = 0.5, min_df = 2)

    ## Training features
    feats = txt2vect.fit_transform(train.tweetTxt)

    ## Bernoulli naive bayes classifier
#    clf = BernoulliNB()

    ## k-Nearest neighbors classifier
#    clf = KNeighborsClassifier()

    ## Multinomial naive bayes classifier
#    clf = MultinomialNB()

    ## Nearest centroid classifier
#    clf = NearestCentroid()

    ## Passive aggressive classifier
#    clf = PassiveAggressiveClassifier()

    ## Perceptron Classifier
#    clf = Perceptron()

    ## Random forest classifier
#    clf = RandomForestClassifier()

    ## Ridge classifier
#    clf = RidgeClassifier()

    ## Stochastic gradient descent classifier
#    clf = SGDClassifier()

    ## Support vector machines classifier
#    clf = svm.SVC(class_weight = {'Achievement': 1, 'Address': 1, 'Appeal': 1,
#                                  'Confrontation': 1, 'Endorsement': 1,
#                                  'Generic': 1, 'Regards': 1, 'Update': 1},
#                  kernel = 'linear')
    clf = svm.SVC(kernel = 'linear')

    ## Print cross-validation results and obtain predictions
    predictions = results.printCV(N_FOLDS, feats, train, clf)

    ## To write predictions to CSV
    predCSV = csv.writer(open('predictions.csv', 'wb', buffering = 0))

    predCSV.writerows(predictions)

    return

if __name__ == '__main__':
    main()
