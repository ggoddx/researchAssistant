from prepClfData import ClfData
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import csv, getSysArgs
import numpy as np
import results


def main():
    ## Number of folds for cross-validation
    N_FOLDS = 5

    ## Training data for classification
    train = ClfData(getSysArgs.usage(['msgTypeClf_gridSearch.py',
                                      '<train_data_filepath>',
                                      '<observation_column_name>',
                                      '<label_column_name>'])[1:])

    train.randomize()

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
                feats = txt2vect.fit_transform(train.tweetTxt)

                for kern in kernGrid:
                    print 'vectorizer:', vectzr, '| max-df:', maxDF, '| min-df:', minDF, '| kernel:', kern

                    ## Support vector machines classifier
                    clf = svm.SVC(kernel = kern)

                    results.printCV(N_FOLDS, feats, train.labels, clf,
                                    gridResults = gridResults, gridParams = [
                            vectzr, maxDF, minDF, kern])

    print np.array(gridResults)

    ## File to write results of grid search
    resCSV = csv.writer(open('gridResults.csv', 'wb', buffering = 0))

    resCSV.writerows(gridResults)

    return

if __name__ == '__main__':
    main()
