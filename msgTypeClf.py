from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold

import csv, getSysArgs
import numpy as np


def main():
    np.random.seed(0)

    ## Training data for classification, observation column name, and label
    #  column name
    [fName, obsCol, lblCol] = getSysArgs.usage(['msgTypeClf.py',
                                                '<train_data_filepath>',
                                                '<observation_column_name>',
                                                '<label_column_name>'])[1:]

    ## Open training data CSV file
    train = list(csv.reader(open(fName, 'rU')))

    ## Column names from training data table
    colNames = train[0]

    train = np.array(train[1:])

    ## Tweet text before removing html entities
    tweetTxtTemp = train[:, colNames.index(obsCol)]

    ## Range of tweet text indicies
    twTxtRange = range(tweetTxtTemp.shape[0])

    ## Tweet text
    tweetTxt = []

    for tweet in tweetTxtTemp:
        ## Tweet cleaned of html entities
        cleanTweet = tweet.replace('&amp;', '&')

        cleanTweet = cleanTweet.replace('&gt;', '>')

        tweetTxt.append(cleanTweet)

    tweetTxt = np.array(tweetTxt)

    del tweetTxtTemp

    ## Labels
    labels = train[:, colNames.index(lblCol)]

    ## Text vectorizer
    txt2vect = CountVectorizer()

    ## Training features
    feats = txt2vect.fit_transform(tweetTxt)

    ## Support vector machines classifier
    clf = svm.SVC()

    ## 5-fold stratified cross-validation
    skf5 = StratifiedKFold(n_splits = 5, shuffle = True)

    ## Data split into folds
    folds = skf5.split(feats, labels)

    for trainIndices, testIndices in folds:
        clf.fit(feats[trainIndices], labels[trainIndices])

        ## True labels
        trueLabels = labels[testIndices]

        ## Predicted labels
        predLabels = clf.predict(feats[testIndices])

        print confusion_matrix(trueLabels, predLabels, labels = [
                'Achievement', 'Address', 'Appeal', 'Confrontation',
                'Endorsement', 'Generic', 'Regards', 'Update'])
        print f1_score(trueLabels, predLabels, average = 'micro')
        print precision_score(trueLabels, predLabels, average = 'micro')
        print recall_score(trueLabels, predLabels, average = 'micro')

    return

if __name__ == '__main__':
    main()
