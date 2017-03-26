import csv, getSysArgs
import numpy as np


def main():
    ## CSV files from source data, previous test data, and previous train data
    [source, prevTest, prevTrain] = getSysArgs.usage(
        ['splitDataFromPrevFile.py', '<source_CSV_filepath>',
         '<previous_test_data_filepath>',
         '<previous_train_data_filepath>'])[1:]

    ## Open previous test data CSV
    prevTest = csv.reader(open(prevTest, 'rU'))

    ## Open previous training data CSV
    prevTrain = csv.reader(open(prevTrain, 'rU'))

    ## Column names from previous test data
    colsPrevTest = prevTest.next()

    ## Column names from previous training data
    colsPrevTrain = prevTrain.next()

    ## Previous test text
    prevTestTxt = {}

    ## Previous training text
    prevTrainTxt = {}

    for row in prevTest:
        prevTestTxt[int(row[colsPrevTest.index('OrigIndex')])] = row[colsPrevTest.index('Text')]

    for row in prevTrain:
        prevTrainTxt[int(row[colsPrevTrain.index('OrigIndex')])] = row[colsPrevTrain.index('Text')]

    ## Open source CSV file
    source = csv.reader(open(source, 'rU'))

    ## Column names from source CSV file
    colNames = source.next()

    ## New test data
    test = [['OrigIndex'] + colNames]

    ## New training data
    train = [['OrigIndex'] + colNames]

    ## Counter for row indices
    ct = 1

    for row in source:
        ## Row for new data split
        newRow = [ct] + row

        ## Index for text column
        txtI = colNames.index('Text')

        if ct in prevTestTxt:
            newRow[txtI] = prevTestTxt[ct]
            test.append(newRow)

        if ct in prevTrainTxt:
            newRow[txtI] = prevTrainTxt[ct]
            train.append(newRow)

        ct += 1

    ## Open new test data CSV
    testCSV = csv.writer(open('testData_20170326.csv', 'wb', buffering = 0))

    ## Open new training data CSV
    trainCSV = csv.writer(open('trainData_20170326.csv', 'wb', buffering = 0))

    testCSV.writerows(test)
    trainCSV.writerows(train)

    return

if __name__ == '__main__':
    main()
