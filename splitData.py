import csv, getSysArgs
import numpy as np

def main():
    ## Open random sequence file (sequence courtesy of random.org)
    seqFile = open('randSeq.txt', 'rU')

    ## List form of permutation in file
    permu = []

    for line in seqFile:
        permu.append(int(line.strip()) + 1)

    ## CSV file of classification data
    [clfFile] = getSysArgs.usage(['splitData.py',
                                 '<classification_data_file_path>'])[1:] 

    ## Open classification data CSV
    clfCSV = np.array(list(csv.reader(open(clfFile, 'rU'))))

    ## Training data
    train = clfCSV[[0] + permu[:6911]]

    ## Test data
    test = clfCSV[[0] + permu[6911:]]

    ## File to which to write training data
    trainCSV = csv.writer(open('trainData.csv', 'wb', buffering = 0))

    ## File to which to write test data
    testCSV = csv.writer(open('testData.csv', 'wb', buffering = 0))

    trainCSV.writerows(train)
    testCSV.writerows(test)

    return

if __name__ == '__main__':
    main()
