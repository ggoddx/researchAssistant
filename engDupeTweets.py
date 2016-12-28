import csv, getSysArgs, re
import numpy as np


def main():
    ## CSV file of Tweets and data
    [fName, twCol] = getSysArgs.usage(['engDupeTweets.py',
                                       '<tweets_CSV_file_path>',
                                       '<tweet_text_col_name>'])[1:]

    ## Open CSV file
    dataCSV = list(csv.reader(open(fName, 'rU')))

    ## Table column names
    colNames = ['OrigIndex'] + dataCSV[0]

    ## List of duplicate tweets
    dupes = np.array(colNames)

    dupes = dupes.reshape(1,dupes.shape[0])
    dataCSV = np.array(dataCSV[1:])
    dataCSV = np.insert(dataCSV, 0, np.arange(dataCSV.shape[0]) + 1, axis = 1)

    ## English data
    dataEng = dataCSV[np.where(dataCSV[:,
                colNames.index('Language')] == 'English')]

    for line in dataEng:
        ## Index of column named Text
        textCol = colNames.index(twCol)

        ## Tweet text
        tweet = line[textCol]

        if tweet not in dupes[:, textCol]:
            ## Rows with tweet text
            potDupes = dataEng[np.where(dataEng[:, textCol] == tweet)]

            if potDupes.shape[0] > 1:
                dupes = np.append(dupes, potDupes, axis = 0)

    ## File to write processed data
    processedCSV = csv.writer(open('engDupeTweets.csv', 'wb', buffering = 0))

    processedCSV.writerows(dupes)

    return

if __name__ == '__main__':
    main()
