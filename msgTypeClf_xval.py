from prepClfData import ClfData
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import StratifiedKFold

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
#    txt2vect = CountVectorizer(binary = True, max_df = 0.99, min_df = 0.01)
    txt2vect = TfidfVectorizer()#max_df = 0.99, min_df = 0.01)

    ## Training features
    feats = txt2vect.fit_transform(train.tweetTxt)

    ## Support vector machines classifier
    clf = svm.SVC(class_weight = {'Achievement': 1, 'Address': 1, 'Appeal': 1,
                                  'Confrontation': 1, 'Endorsement': 1,
                                  'Generic': 1, 'Regards': 1, 'Update': 1},
                  kernel = 'linear')

    results.printCV(N_FOLDS, feats, train.labels, clf)

    return

if __name__ == '__main__':
    main()
