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
    [fName, obsCol, lblCol] = getSysArgs.usage(['msgTypeClf_gridSearch.py',
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

    ## 5-fold stratified cross-validation
    skf5 = StratifiedKFold(n_splits = N_FOLDS)

    ## Grid for vectorizer
    txt2vectGrid = ['binary', 'count', 'tf', 'tfidf']

    ## Grid for maximum document frequencies
    maxDFgrid = [0.99, 1.0]

    ## Grid for minimum document frequencies
    minDFgrid = [0.01, 1]

    ## Grid for kernels
    kernGrid = ['rbf', 'linear', 'poly', 'sigmoid']

    ## F1-scores from each fold for each grid result
    gridResults = [['vectorizer', 'max-df', 'min-df', 'kernel', 'F1-score_1',
                    'F1-score_2', 'F1-score_3', 'F1-score_4', 'F1-score_5']]

    for vectzr in txt2vectGrid:
        for maxDF in maxDFgrid:
            for minDF in minDFgrid:
                ## Text vectorizer
                txt2vect = None

                if vectzr == 'binary':
                    txt2vect = CountVectorizer(binary = True, max_df = maxDF,
                                               min_df = minDF)
                elif vectzr == 'count':
                    txt2vect = CountVectorizer(binary = False, max_df = maxDF,
                                               min_df = minDF)
                elif vectzr == 'tf':
                    txt2vect = TfidfVectorizer(max_df = maxDF, min_df = minDF,
                                               use_idf = False)
                elif vectzr == 'tfidf':
                    txt2vect = TfidfVectorizer(max_df = maxDF, min_df = minDF,
                                               use_idf = True)

                ## Training features
                feats = txt2vect.fit_transform(tweetTxt)

                for kern in kernGrid:
                    print 'vectorizer:', vectzr, '| max-df:', maxDF, '| min-df:', minDF, '| kernel:', kern

                    ## Support vector machines classifier
                    clf = svm.SVC(kernel = kern)

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

                        cvCM.append(confusion_matrix(trueLabels, predLabels, labels = ['Achievement', 'Address', 'Appeal', 'Confrontation', 'Endorsement', 'Generic', 'Regards', 'Update']))

                        print 'Fold', fold, 'of', N_FOLDS, 'complete'
                        fold += 1

                    gridResults.append([vectzr, maxDF, minDF, kern] + cvF1)

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

    print np.array(gridResults)

    ## File to write results of grid search
    resCSV = csv.writer(open('gridResults.csv', 'wb', buffering = 0))

    resCSV.writerows(gridResults)

    return

if __name__ == '__main__':
    main()
