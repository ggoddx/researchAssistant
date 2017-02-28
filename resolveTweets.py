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

    ## non-ASCII file column names
    nAcolNames = nonASCII.next()

    nonASCII = np.array(list(nonASCII))
    nonASCII = nonASCII[np.where(nonASCII[:,
                nAcolNames.index('non-ASCIIlen')] != '0')]

    ## Fixed text
    fixed = {}

    for line in nonASCII:
        ## To fixed encoding issues in tweet
        tweet = line[nAcolNames.index(twCol)]

        tweet = tweet.decode(chardet.detect(tweet)['encoding'])
        tweet = ftfy.fix_text(tweet)
        tweet = tweet.replace(u'\xe2\x80\u015a', '...')
        tweet = tweet.replace(u'\xe2\x80\x98', "'")
        tweet = tweet.replace(u'\u0111\x9f\x98\x81', u'\U0001F601')
        tweet = tweet.replace(u'\u0111\x9f\x98\x8a', u'\U0001F60A')
        tweet = tweet.replace(u'\u0111\x9f\x98\x8d', u'\U0001F60D')
        tweet = tweet.replace(u'\u0111\x9f\x91\x8c', u'\U0001F44C')
        tweet = tweet.replace(u'\xe2\x80\x93', '-')
        tweet = tweet.replace(u'\x82', '')
        tweet = tweet.replace(u'\u0102\x9f', u'\u00DF')
        tweet = tweet.replace(u'\u0102\xa4', u'\u00E4')
        tweet = tweet.replace(u'\u0102\xc2\xa0', '')
        tweet = tweet.replace(u'\u0102\u0141', u'\u00E3')
        tweet = tweet.replace(u'\u0102\u02d8\xe2\u0179\u0139\x93', '"')
        tweet = tweet.replace(u'\u0102\u02d8\xe2\u0179\xc2\u015a', '...')

#        if float(line[nAcolNames.index('%non-ASCII')]) < 0.3:
        fixed[line[nAcolNames.index('OrigIndex')]] = tweet

#        if re.search('\x82', tweet) != None:
#            print [tweet]

#    print fixed
#    print [fixed['6275']]
#    print fixed['6275']

    c = 0
    for i in fixed:
        if fixed[i].find(u'\u0102') >= 0:
            print i, fixed[i]
            print [fixed[i]]
            c += 1
#            print fixed[i].replace(u'\xe2\x80\u015a','...')
#    print fixed['6234'].find(u'\xe2\x80\u015a')

    print c

    return

    ## Open CSV file
    dataCSV = csv.reader(open(fName, 'rU'))

    ## Table column names
    colNames = dataCSV.next()

    dataCSV = np.array(list(dataCSV))

    line = dataCSV[3]

    ## Tweet
    tweet = line[colNames.index(twCol)]

    print tweet
    tweet = tweet.decode(chardet.detect(tweet)['encoding'])
    tweet = ftfy.fix_text(tweet)
    print tweet

    fixedCSV = csv.writer(open('fixed.csv', 'wb', buffering = 0))
    fixedCSV.writerows([[tweet]])
    '''for line in dataCSV:
        ## Tweet
        tweet = line[colNames.index(twCol)]

        tweet = tweet.decode(chardet.detect(tweet)['encoding'])
#        print unicode(tweet)
        print ftfy.fix_text(unicode(tweet))
        break'''

    return

if __name__ == '__main__':
    main()
