import csv, getSysArgs, re
import numpy as np


def main():
    ## CSV file of Tweets and data
    [fName] = getSysArgs.usage(['engTweetNonASCII.py',
                                '<tweets_CSV_file_path>'])[1:]

    ## Open CSV file
    dataCSV = list(csv.reader(open(fName, 'rU')))

    ## Table column names
    colNames = ['OrigIndex'] + dataCSV[0]

    ## List of non-ASCII characters
    nonASCII = [['OrigIndex', 'Text', 'non-ASCII', 'TextLen', 'non-ASCIIlen',
                 '%non-ASCII']]

    dataCSV = np.array(dataCSV[1:])
    dataCSV = np.insert(dataCSV, 0, np.arange(dataCSV.shape[0]) + 1, axis = 1)

    ## English data
    dataEng = dataCSV[np.where(dataCSV[:,
                colNames.index('Language')] == 'English')]

    for line in dataEng:
        ## Index of column named Text
        textCol = colNames.index('Text')

        ## Tweet text
        tweet = line[textCol]

        ## non-ASCII characters in tweet
        nonASCIIchars = re.sub('[ -~]', '', tweet)

        ## Length of tweet
        twLen = len(tweet)

        ## Number of non-ASCII characters in tweet
        numNonASCII = len(nonASCIIchars)

        nonASCII.append([line[0], tweet, nonASCIIchars, twLen, numNonASCII,
                         numNonASCII/ float(twLen)])

    ## File to write processed data
    processedCSV = csv.writer(open('engTweetNonASCII.csv',
                                   'wb', buffering = 0))

    processedCSV.writerows(nonASCII)

    return

if __name__ == '__main__':
    main()
