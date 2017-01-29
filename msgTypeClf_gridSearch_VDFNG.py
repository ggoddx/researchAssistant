from prepClfData import ClfData
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
#from sklearn.metrics import confusion_matrix, f1_score
#from sklearn.model_selection import StratifiedKFold

import csv, getSysArgs
import numpy as np
import results


def main():
    ## Number of folds for cross-validation
    N_FOLDS = 5

    ## Training data for classification
    train = ClfData(getSysArgs.usage(['msgTypeClf_gridSearch_VNG.py',
                                      '<train_data_filepath>',
                                      '<observation_column_name>',
                                      '<label_column_name>'])[1:])

    train.randomize()

    ## Grid for vectorizer
    txt2vectGrid = ['binary']#, 'count', 'tf', 'tfidf']

    ## Grid for maximum document frequencies
    maxDFgrid = [0.9, 0.95, 0.98, 0.99, 1.0]

    ## Grid for minimum document frequencies
    minDFgrid = [1, 2, 5, 10]

    ## Grid for n-grams
    ngramGrid = [(1, 2)]#(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]

    ## F1-scores from each fold for each grid result
    gridResults = [['vectorizer', 'max-df', 'min-df', 'n-gramRange',
                    'F1-score_1', 'F1-score_2', 'F1-score_3', 'F1-score_4',
                    'F1-score_5']]

    for vectzr in txt2vectGrid:
        for maxDF in maxDFgrid:
            for minDF in minDFgrid:
                for ngramRange in ngramGrid:
                    print 'vectorizer:', vectzr, '| max-df:', maxDF, '| min-df:', minDF, '| n-gram:', ngramRange

                    ## Text vectorizer
                    txt2vect = None

                    if vectzr == 'binary':
                        txt2vect = CountVectorizer(
                            binary = True, ngram_range = ngramRange,
                            max_df = maxDF, min_df = minDF)

                    elif vectzr == 'count':
                        txt2vect = CountVectorizer(
                            binary = False, ngram_range = ngramRange,
                            max_df = maxDF, min_df = minDF)

                    elif vectzr == 'tf':
                        txt2vect = TfidfVectorizer(
                            ngram_range = ngramRange, max_df = maxDF,
                            min_df = minDF, use_idf = False)

                    elif vectzr == 'tfidf':
                        txt2vect = TfidfVectorizer(
                            ngram_range = ngramRange, max_df = maxDF,
                            min_df = minDF, use_idf = True)

                    ## Training features
                    feats = txt2vect.fit_transform(train.tweetTxt)

                    ## Support vector machines classifier
                    clf = svm.SVC(kernel = 'linear')

                    results.printCV(N_FOLDS, feats, train.labels, clf,
                                    gridResults = gridResults, gridParams = [
                            vectzr, maxDF, minDF, str(ngramRange)])

    print np.array(gridResults)

    ## File to write results of grid search
    resCSV = csv.writer(open('gridResults.csv', 'wb', buffering = 0))

    resCSV.writerows(gridResults)

    return

if __name__ == '__main__':
    main()
