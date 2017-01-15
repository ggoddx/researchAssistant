from prepClfData import ClfData
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import StratifiedKFold

import csv, getSysArgs
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
#    txt2vect = CountVectorizer(binary = True, max_df = 0.99, min_df = 0.01)
    txt2vect = TfidfVectorizer()#max_df = 0.99, min_df = 0.01)

    ## Training features
    feats = txt2vect.fit_transform(train.tweetTxt)

    ## Support vector machines classifier
    clf = svm.SVC(class_weight = {'Achievement': 1, 'Address': 1, 'Appeal': 1,
                                  'Confrontation': 1, 'Endorsement': 1,
                                  'Generic': 1, 'Regards': 1, 'Update': 1},
                  kernel = 'linear')

    ## 5-fold stratified cross-validation
    skf5 = StratifiedKFold(n_splits = N_FOLDS)

    ## Data split into folds
    folds = skf5.split(feats, train.labels)

    ## F1-scores from cross-validation
    cvF1 = []

    ## Confusion matricies from cross-validation
    cvCM = []

    ## Counter for fold iterations
    fold = 1

    for trainIndices, testIndices in folds:
        clf.fit(feats[trainIndices], train.labels[trainIndices])

        ## True labels
        trueLabels = train.labels[testIndices]

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
