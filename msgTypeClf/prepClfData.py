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
        data = csv.reader(open(fName, 'rU'))

        ## Column names from classification data table
        colNames = data.next()

        ## Tweet text
        tweetTxt = []

        ## Classification labels
        labels = []

        for row in data:
            ## Tweet cleaned of HTML entities
            tweet = row[colNames.index(obsCol)].replace('&amp;', '&')

            tweet = tweet.replace('&gt;', '>')
            tweetTxt.append(tweet)

            ## Label for row
            label = row[colNames.index(lblCol)]

            labels.append(label)

        self.tweetTxt = np.array(tweetTxt)
        self.labels = np.array(labels)

        return

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

        return
