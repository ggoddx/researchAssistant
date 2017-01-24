from keras.layers import Activation, Dense, Dropout
from keras.models import Sequential
from prepClfData import ClfData
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
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

    ## Multi-layer perceptron classifier
    clf = Sequential()

    clf.add(Dense(512, input_shape = (feats.shape[1],)))
    clf.add(Activation('relu'))
    clf.add(Dropout(0.5))
    clf.add(Dense(labels.shape[1]))
    clf.add(Activation('softmax'))

    clf.compile(loss = 'categorical_crossentropy', optimizer = 'adam',
                metrics = ['accuracy'])

    x_train = feats[:5588]
    y_train = labels[:5588]
    x_test = feats[5588:]
    y_test = train.labels[5588:]

    history = clf.fit(x_train.todense(), y_train, nb_epoch = 5,
                      batch_size = 32, verbose = 1, validation_split = 0.1)

    y_pred_dist = clf.predict(x_test.todense(), batch_size = 32, verbose = 1)

    y_pred = []

    for i in range(y_pred_dist.shape[0]):
        y_pred.append(lb.classes_[np.argmax(y_pred_dist[i])])

    y_pred = np.array(y_pred)
    print '\n', confusion_matrix(y_test, y_pred)

    return

if __name__ == '__main__':
    main()
