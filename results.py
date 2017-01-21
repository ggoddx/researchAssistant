from sklearn.metrics import confusion_matrix, f1_score
from sklearn.metrics import precision_recall_fscore_support as prfs
from sklearn.model_selection import StratifiedKFold

import numpy as np


## Runs cross-validation of classification model and prints results
#  @param n_folds int
#   number of folds for cross validation
#
#  @param feats numpy array
#   text-feature matrix of tweets
#
#  @param labels numpy array
#   label for each tweet
#
#  @param clf sci-kit learn classifier object
#   classification model
def printCV(n_folds, feats, labels, clf):
    ## 5-fold stratified cross-validation
    skf5 = StratifiedKFold(n_splits = n_folds)

    ## Data split into folds
    folds = skf5.split(feats, labels)

    ## List of labels
    lbls = ['Achievement', 'Address', 'Appeal', 'Confrontation', 'Endorsement',
            'Generic', 'Regards', 'Update']

    ## F1-scores from cross-validation
    cvF1 = []

    ## Confusion matricies from cross-validation
    cvCM = []

    ## Label-level results from cross-validation
    cvLblRes = []

    ## Counter for fold iterations
    fold = 1

    for trainIndices, testIndices in folds:
        clf.fit(feats[trainIndices], labels[trainIndices])

        ## True labels
        trueLabels = labels[testIndices]

        ## Predicted labels
        predLabels = clf.predict(feats[testIndices])

        cvF1.append(f1_score(trueLabels, predLabels, average = 'micro'))

        cvCM.append(confusion_matrix(trueLabels, predLabels, labels = lbls))

        cvLblRes.append(np.transpose(np.array(prfs(trueLabels, predLabels,
                                                   labels = lbls))))

        print 'Fold', fold, 'of', n_folds, 'complete'
        fold += 1

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

    return
