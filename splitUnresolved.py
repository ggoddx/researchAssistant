import csv, getSysArgs, re
import numpy as np

def main():
    ## CSV file of Tweets and data, non-ASCII tweet analysis, and duplicates
    [fName,
     nonASCIIcsv,
     dupeCSV] = getSysArgs.usage(['splitUnresolved.py',
                                  '<tweets_CSV_file_path>',
                                  '<non-ASCII_CSV_file_path>',
                                  '<duplicates_CSV_file_path>'])[1:]

    ## Open CSV file of Tweets
    dataCSV = list(csv.reader(open(fName, 'rU')))

    ## Open CSV file of non-ASCII tweet analysis
    nonASCII = list(csv.reader(open(nonASCIIcsv, 'rU')))

    ## Open CSV file of duplicate tweets
    dupes = np.array(list(csv.reader(open(dupeCSV, 'rU'))))

    ## Table column names
    colNames = ['OrigIndex'] + dataCSV[0]

    ## Tweets with no discrepancies
    res = [colNames]

    ## Tweets with discrepancies that need to be resolved
    unres = [colNames]

    dataCSV = np.array(dataCSV[1:])
    dataCSV = np.insert(dataCSV, 0, np.arange(dataCSV.shape[0]) + 1, axis = 1)

    ## English data
    dataEng = dataCSV[np.where(dataCSV[:,
                colNames.index('Language')] == 'English')]

    ## Non-ASCII analysis column names
    nonASCIIcols = nonASCII[0]

    nonASCII = np.array(nonASCII[1:])
    nonASCII = nonASCII[np.where(nonASCII[:,
                nonASCIIcols.index('non-ASCIIlen')] != '0')]

    ## Range of rows in English data
    engRange = range(dataEng.shape[0])

    for i in engRange:
        ## row of English data
        row = list(dataEng[i])

        ## Original index
        origI = row[0]

        if origI in nonASCII[:, 0] or origI in dupes[:, 0]:
            unres.append(row)
        else:
            res.append(row)

    ## File to write data with no discrepancies
    resCSV = csv.writer(open('resolvedData.csv', 'wb', buffering = 0))

    ## File to write unresolved data
    unresCSV = csv.writer(open('unresolvedData.csv', 'wb', buffering = 0))

    resCSV.writerows(res)
    unresCSV.writerows(unres)

    return

if __name__ == '__main__':
    main()
