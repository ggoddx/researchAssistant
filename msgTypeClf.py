import csv, getSysArgs
import numpy as np

def main():
    np.random.seed(0)

    ## Training data for classification, observation column name, and label
    #  column name
    [fName, obsCol, lblCol] = getSysArgs.usage(['msgTypeClf.py',
                                                '<train_data_filepath>',
                                                '<observation_column_name>',
                                                '<label_column_name>'])[1:]

    ## Open training data CSV file
    train = list(csv.reader(open(fName, 'rU')))

    ## Column names from training data table
    colNames = train[0]

    train = np.array(train[1:])

    ## Tweet text
    tweetTxt = train[:, colNames.index(obsCol)]

    ## Labels
    labels = train[:, colNames.index(lblCol)]

    print labels
    print labels.shape

    return

if __name__ == '__main__':
    main()
