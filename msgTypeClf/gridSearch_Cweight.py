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
    train = ClfData(getSysArgs.usage(['msgTypeClf_gridSearch.py',
                                      '<train_data_filepath>',
                                      '<observation_column_name>',
                                      '<label_column_name>'])[1:])

    train.randomize()

    ## Text vectorizer
    txt2vect = TfidfVectorizer()

    ## Training features
    feats = txt2vect.fit_transform(train.tweetTxt)

    ## Grid for label weights
    lblWtGrid = [1, 10]

    ## F1-scores from each fold for each grid result
    gridResults = [['Achievement', 'Address', 'Appeal', 'Confrontation',
                    'Endorsement', 'Generic', 'Regards', 'Update',
                    'F1-score_1', 'F1-score_2', 'F1-score_3', 'F1-score_4',
                    'F1-score_5']]

    for wtAc in lblWtGrid:
        for wtAd in lblWtGrid:
            for wtAp in lblWtGrid:
                for wtCo in lblWtGrid:
                    for wtEn in lblWtGrid:
                        for wtGe in lblWtGrid:
                            for wtRe in lblWtGrid:
                                for wtUp in lblWtGrid:
                                    print 'Achievement', wtAc, 'Address', wtAd, 'Appeal', wtAp, 'Confrontation', wtCo, 'Endorsement', wtEn, 'Generic', wtGe, 'Regards', wtRe, 'Update', wtUp

                                    ## Support vector machines classifier
                                    clf = svm.SVC(class_weight = {
                                            'Achievement': wtAc,
                                            'Address': wtAd, 'Appeal': wtAp,
                                            'Confrontation': wtCo,
                                            'Endorsement': wtEn,
                                            'Generic': wtGe, 'Regards': wtRe,
                                            'Update': wtUp}, kernel = 'linear')

                                    results.printCV(N_FOLDS, feats,
                                                    train.labels, clf,
                                                    gridResults = gridResults,
                                                    gridParams = [
                                            wtAc, wtAd, wtAp, wtCo, wtEn, wtGe,
                                            wtRe, wtUp])

    print np.array(gridResults)

    ## File to write results of grid search
    resCSV = csv.writer(open('gridResults.csv', 'wb', buffering = 0))

    resCSV.writerows(gridResults)

    return

if __name__ == '__main__':
    main()
