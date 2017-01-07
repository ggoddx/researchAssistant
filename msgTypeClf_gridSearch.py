from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import StratifiedKFold

import csv, getSysArgs
import numpy as np


def main():
    np.random.seed(0)

    ## Number of folds for cross-validation
    N_FOLDS = 5

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

    ## Support vector machines classifier
    clf = svm.SVC(kernel = 'linear')

    ## 5-fold stratified cross-validation
    skf5 = StratifiedKFold(n_splits = N_FOLDS, shuffle = True)

    ## Grid for maximum and minimum document frequencies
    dfGrid = [0.001, 0.01, 0.02, 0.05, 0.1]

    for maxDF in dfGrid:
        for minDF in dfGrid:
            print 'max-df', 1 - maxDF, '| min-df', minDF

            ## Text vectorizer
            txt2vect = CountVectorizer(max_df = 0.99, min_df = 0.01)

            ## Training features
            feats = txt2vect.fit_transform(tweetTxt)

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

                cvF1.append(f1_score(trueLabels, predLabels,
                                     average = 'micro'))

                cvCM.append(confusion_matrix(trueLabels, predLabels, labels = [
                            'Achievement', 'Address', 'Appeal',
                            'Confrontation', 'Endorsement', 'Generic',
                            'Regards', 'Update']))

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
