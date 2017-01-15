from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import StratifiedKFold

import csv, getSysArgs
import numpy as np


def main():
    ## Number of folds for cross-validation
    N_FOLDS = 5

    ## Training data for classification, observation column name, and label
    #  column name
    [fName, obsCol, lblCol] = getSysArgs.usage(['msgTypeClf_xval.py',
                                                '<train_data_filepath>',
                                                '<observation_column_name>',
                                                '<label_column_name>'])[1:]

    ## Open training data CSV file
    train = list(csv.reader(open(fName, 'rU')))

    ## Column names from training data table
    colNames = train[0]

    train = np.array(train[1:])

    ## Open random sequence file (courtesy of random.org)
    seqFile = open('trainRandSeq.txt', 'rU')

    ## List form of permutation in file
    permu = []

    for line in seqFile:
        permu.append(int(line.strip()))

    train = train[permu]

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
#    txt2vect = CountVectorizer(binary = True, max_df = 0.99, min_df = 0.01)
    txt2vect = TfidfVectorizer()#max_df = 0.99, min_df = 0.01)

    ## Training features
    feats = txt2vect.fit_transform(tweetTxt)

    ## Support vector machines classifier
    clf = svm.SVC(class_weight = {'Achievement': 1, 'Address': 1, 'Appeal': 1,
                                  'Confrontation': 1, 'Endorsement': 1,
                                  'Generic': 1, 'Regards': 1, 'Update': 1},
                  kernel = 'linear')

    ## 5-fold stratified cross-validation
    skf5 = StratifiedKFold(n_splits = N_FOLDS)

    ## Data split into folds
    folds = skf5.split(feats, labels)

    ## F1-scores from cross-validation
    cvF1 = []

    ## Confusion matricies from cross-validation
    cvCM = []

    ## Counter for fold iterations
    fold = 1

    for trainIndices, testIndices in folds:
        clf.fit(feats[trainIndices], labels[trainIndices])

        ## True labels
        trueLabels = labels[testIndices]

        ## Predicted labels
        predLabels = clf.predict(feats[testIndices])

        cvF1.append(f1_score(trueLabels, predLabels, average = 'micro'))

        cvCM.append(confusion_matrix(trueLabels, predLabels, labels = [
                    'Achievement', 'Address', 'Appeal', 'Confrontation',
                    'Endorsement', 'Generic', 'Regards', 'Update']))

        print 'Fold', fold, 'of', N_FOLDS, 'complete'
        fold += 1

    cvF1 = np.array(cvF1)
    print cvF1
    print 'mean: ', np.mean(cvF1)
    print 'min: ', np.min(cvF1)
    print 'median: ', np.median(cvF1)
    print 'max: ', np.max(cvF1)
    print 'mean confusion matrix'
    print np.mean(np.array(cvCM), axis = 0)

    for cm in cvCM:
        print cm

    return

if __name__ == '__main__':
    main()
