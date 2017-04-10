from sklearn.metrics import confusion_matrix, f1_score
from sklearn.metrics import precision_recall_fscore_support as prfs
from sklearn.model_selection import StratifiedKFold

import numpy as np


## Runs cross-validation of classification model and prints results
#
#  @param n_folds int
#   number of folds for cross validation
#
#  @param feats numpy array
#   text-feature matrix of tweets
#
#  @param train ClfData object
#   contains labels, original indices, and tweet text from training data
#
#  @param clf sci-kit learn classifier object
#   classification model
#
#  @param gridResults list
#   list of results from grid search
#   (for use with prininting results during a grid search)
#
#  @param gridParams list
#   parameters involved in the point of the grid search
#   (for use with prininting results during a grid search)
#
#  @returns predictions list
#   list of lists containing predicted labels for each tweet
def printCV(n_folds, feats, train, clf, gridResults = None, gridParams = None):
    ## 5-fold stratified cross-validation
    skf5 = StratifiedKFold(n_splits = n_folds)

    ## Data split into folds
    folds = skf5.split(feats, train.labels)

    ## List of labels
    lbls = ['Achievement', 'Address', 'Appeal', 'Confrontation', 'Endorsement',
            'Generic', 'Regards', 'Update']

    ## F1-scores from cross-validation
    cvF1 = []

    ## Confusion matricies from cross-validation
    cvCM = []

    ## Label-level results from cross-validation
    cvLblRes = []

    ## To store predictions
    predictions = [['OrigIndex', 'Text', 'True Message Type',
                    'Predicted Message Type']]

    ## Counter for fold iterations
    fold = 1

    for trainIndices, testIndices in folds:
        ## Original indices
        origIs = train.indices[testIndices]

        ## Tweet text
        tweet = train.tweetTxt[testIndices]

        ## True labels
        trueLabels = train.labels[testIndices]

        clf.fit(feats[trainIndices], train.labels[trainIndices])

        ## Predicted labels
        predLabels = clf.predict(feats[testIndices])

        for i in range(origIs.shape[0]):
            predictions.append([origIs[i], tweet[i], trueLabels[i],
                                predLabels[i]])

        cvF1.append(f1_score(trueLabels, predLabels, average = 'micro'))
        cvCM.append(confusion_matrix(trueLabels, predLabels, labels = lbls))

        cvLblRes.append(np.transpose(np.array(prfs(trueLabels, predLabels,
                                                   labels = lbls))))

        print 'Fold', fold, 'of', n_folds, 'complete'
        fold += 1

    if gridResults is not None:
        gridResults.append(gridParams + cvF1)

    cvF1 = np.array(cvF1)
    print cvF1
    print 'mean: ', np.mean(cvF1)
    print 'min: ', np.min(cvF1)
    print 'median: ', np.median(cvF1)
    print 'max: ', np.max(cvF1)
    print 'mean confusion matrix'
    print np.mean(np.array(cvCM), axis = 0)
    print 'mean label-level statistics'
    print np.mean(np.array(cvLblRes), axis = 0)

    for cm in cvCM:
        print cm

    return predictions
