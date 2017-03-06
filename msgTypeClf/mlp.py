from keras.layers import Activation, Dense, Dropout
from keras.models import Sequential
from prepClfData import ClfData
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.metrics import precision_recall_fscore_support as prfs
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelBinarizer

import csv, getSysArgs
import numpy as np
import results


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
    txt2vect = TfidfVectorizer()

    ## Training features
    feats = txt2vect.fit_transform(train.tweetTxt)

    ## To binarize labels
    lb = LabelBinarizer()

    ## Training labels (as binarized matrix)
    labels = lb.fit_transform(train.labels)

    ## 5-fold stratified cross-validation
    skf5 = StratifiedKFold(n_splits = N_FOLDS)

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

    ## Counter for fold iterations
    fold = 1

    for trainIndices, testIndices in folds:
        ## Multi-layer perceptron classifier
        clf = Sequential()

        clf.add(Dense(512, input_shape = (feats.shape[1],)))
        clf.add(Activation('relu'))
        clf.add(Dropout(0.5))
        clf.add(Dense(labels.shape[1]))
        clf.add(Activation('softmax'))

        clf.compile(loss = 'categorical_crossentropy', optimizer = 'adam',
                    metrics = ['accuracy'])

        clf.fit(feats[trainIndices].todense(), labels[trainIndices],
                nb_epoch = 5, batch_size = 32, verbose = 1,
                validation_split = 0.1)

        ## True labels
        trueLabels = train.labels[testIndices]

        ## Prediction distribution
        predDist = clf.predict(feats[testIndices].todense(), batch_size = 32,
                               verbose = 1)

        ## Predicted labels
        predLabels = []

        for i in range(predDist.shape[0]):
            predLabels.append(lb.classes_[np.argmax(predDist[i])])

        predLabels = np.array(predLabels)

        cvF1.append(f1_score(trueLabels, predLabels, average = 'micro'))
        cvCM.append(confusion_matrix(trueLabels, predLabels, labels = lbls))

        cvLblRes.append(np.transpose(np.array(prfs(trueLabels, predLabels,
                                                   labels = lbls))))

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
    print 'mean label-level statistics'
    print np.mean(np.array(cvLblRes), axis = 0)

    for cm in cvCM:
        print cm

    return

if __name__ == '__main__':
    main()
