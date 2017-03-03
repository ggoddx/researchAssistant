import chardet, csv, ftfy, getSysArgs, re
import numpy as np


def main():
    ## CSV file of Tweets and data
    [fName, twCol] = getSysArgs.usage(['resolveTweets.py',
                                       '<tweets_CSV_file_path>',
                                       '<tweet_text_col_name>'])[1:]

    ## Open non-ASCII tweet file
    nonASCII = csv.reader(open('./Discrepancy Analysis/engTweetNonASCII.csv',
                               'rU'))

    ## Non-ASCII file column names
    nAcolNames = nonASCII.next()

    nonASCII = np.array(list(nonASCII))
    nonASCII = nonASCII[np.where(nonASCII[:,
                nAcolNames.index('non-ASCIIlen')] != '0')]

    ## Non-English tweets labeled as English
    nonEngFile = open('./Discrepancy Analysis/nonEnglishTweets.txt', 'rU')

    ## List of non-English tweets
    nonEng = []

    for line in nonEngFile:
        nonEng.append(line.strip())

    del nonEngFile

    ## Temporary list for non-ASCII tweets to remove non-English tweets
    nonASCIItemp = []

    for line in nonASCII:
        if line[nAcolNames.index('OrigIndex')] not in nonEng:
            nonASCIItemp.append(line)

    nonASCII = np.array(nonASCIItemp)

    del nonASCIItemp

    ## Fixed text
    fixed = {}

    for line in nonASCII:
        ## To fixed encoding issues in tweet
        tweet = line[nAcolNames.index(twCol)]

        tweet = tweet.decode(chardet.detect(tweet)['encoding'])
        tweet = ftfy.fix_text(tweet)
        tweet = tweet.replace(u'\xe2\x80\u015a', '...')  #fixes 322 tweets
        tweet = tweet.replace(u'\u2026', '...')  #fixes 181 tweets
        tweet = tweet.replace(u'\u2013', '-')  #fixes 20 tweets
        tweet = tweet.replace(u'\u2014', '-')  #fixes 13 tweets
        tweet = tweet.replace(u'\u0111\x9f\x98\x8a', u'\U0001F60A')  #fixes 2
        tweet = tweet.replace(u'\u0102\x82\xc2\xa0', '')  #fixes 2 tweets
        tweet = tweet.replace(u'\xa0', ' ')  #fixes 28 tweets
        tweet = tweet.replace(u'\u0102\x82', '')  #fixes 13 tweets
        tweet = tweet.replace(u'\u0111\x9f\x91\x8c', u'\U0001F44C')  #fixes 1
        tweet = tweet.replace(u'\u0111\x9f\x98\x81', u'\U0001F601')  #fixes 1
        tweet = tweet.replace(u'\u0111\x9f\x98\x8d', u'\U0001F60D')  #fixes 1
        tweet = tweet.replace(u'\u02d8\xe2\x82\u0179\xc2\u015a', '...')  #fix 1
        tweet = tweet.replace(u'\xc2', '')  #fixes 9 tweets
        tweet = tweet.replace(u'\u0102\xa4', u'\u00E4')  ## fixes 1 tweet
        tweet = tweet.replace(u'\u0111\x9f\x92\x98', u'\U0001F498')  ## fixes 1
        tweet = tweet.replace(u'\u0111\x9f\x98\x98', u'\U0001F618')  ## fixes 1
        tweet = tweet.replace(u'\u2015', '-')  #fixes 1 tweet
        tweet = tweet.replace(u'\u0102\u0141', u'\u00E3')  #fixes 1 tweet
        tweet = tweet.replace(u'\u0102\u02d8\xe2\x82\u0179\u0139\x93', '"')  #1
        tweet = tweet.replace(u'\u0102\u017a', u'\u00FC')  #fixes 1 tweet
        tweet = tweet.replace(u'\u0102', '')  #fixes 1 tweet
        tweet = tweet.replace(u'\xe2\x80\x94', '-')  #fixes 1 tweet
        tweet = tweet.replace(u'\xe2\x80\x98', "'")  #fixes 1 tweet
        tweet = tweet.replace(u'\xe2\x80\x93', '-')  #fixes 1 tweet

        fixed[line[nAcolNames.index('OrigIndex')]] = tweet

    del nonASCII
    del nAcolNames

    ## Open CSV file
    dataCSV = csv.reader(open(fName, 'rU'))

    ## Table column names
    colNames = dataCSV.next()

    ## Training indicies for remaining unresolved tweets
    trainIs = np.array(list(csv.reader(
        open('./Unresolved Data/trainIndicies_for20170301.csv',
             'rU')))).reshape((735,))

    ## Test indicies for remaining unresolved tweets
    testIs = np.array(list(csv.reader(
                open('./Unresolved Data/testIndicies_for20170301.csv',
                     'rU')))).reshape((82,))

    ## Training data from unresolved tweets
    train = []

    ## Test data from unresolved tweets
    test = []

    ## Counter
    c = 1

    for row in dataCSV:
        ## Index from full dataset
        i = str(c)

        if i in trainIs:
            row[colNames.index(twCol)] = fixed[i].encode('utf-8')
            train.append([i] + row)

        if i in testIs:
            row[colNames.index(twCol)] = fixed[i].encode('utf-8')
            test.append([i] + row)

        c += 1

    del fixed
    del dataCSV
    del colNames
    del trainIs
    del testIs

    ## Open train data file
    trainCSV = list(csv.reader(
            open('./Classification Data/trainData_20161228.csv', 'rU')))

    ## Open test data file
    testCSV = list(csv.reader(
            open('./Classification Data/testData_20161228.csv', 'rU')))

    ## File to write new train data
    newTrain = csv.writer(open('./Classification Data/trainData_20170303.csv',
                               'wb', buffering = 0))

    ## File to write new test data
    newTest = csv.writer(open('./Classification Data/testData_20170303.csv',
                              'wb', buffering = 0))

    newTrain.writerows(trainCSV + train)
    newTest.writerows(testCSV + test)

    return

if __name__ == '__main__':
    main()
