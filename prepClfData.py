import csv
import numpy as np


## Handles gathering of data needed for classification tasks
class ClfData:
    ## Establishes ClfData object
    #
    #  @param fileSpecs list
    #   list of variables needed to find file with classification data
    #   (currently ordered as [filename, observations_col, labels_col])
    def __init__(self, fileSpecs):
        ## File specifications
        [fName, obsCol, lblCol] = fileSpecs

        ## Open classification data CSV file
        data = list(csv.reader(open(fName, 'rU')))

        ## Column names from classification data table
        colNames = data[0]

        data = np.array(data[1:])

        ## Tweet text before removing html entities
        tweetTxtTemp = data[:, colNames.index(obsCol)]

        ## Range of tweet text indicies
        twTxtRange = range(tweetTxtTemp.shape[0])

        ## Tweet text
        self.tweetTxt = []

        for tweet in tweetTxtTemp:
            ## Tweet cleaned of HTML entities
            cleanTweet = tweet.replace('&amp;', '&')

            cleanTweet = cleanTweet.replace('&gt;', '>')
            self.tweetTxt.append(cleanTweet)

        self.tweetTxt = np.array(self.tweetTxt)

        del tweetTxtTemp

        ## Classification labels
        self.labels = data[:, colNames.index(lblCol)]

    ## Randomizes classification data (for cases like cross-validation)
    def randomize(self):
        ## Open random sequence file (courtesy of random.org)
        seqFile = open('trainRandSeq.txt', 'rU')

        ## List form of permutation in file
        permu = []

        for line in seqFile:
            permu.append(int(line.strip()))

        self.tweetTxt = self.tweetTxt[permu]
        self.labels = self.labels[permu]
