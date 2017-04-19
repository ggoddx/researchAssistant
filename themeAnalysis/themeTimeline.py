from copy import deepcopy as dcp
from dateutil.parser import parse

import csv, getSysArgs


## Adds zeroes to the counts of themes that appear later in time in dataset
#
#  @param theme tuple
#   theme-type, theme-name pair that identifies theme / message type
#
#  @param themeCts dict
#   stores various counts for various timeframes
#
#  @param zeroes dict
#   lists of zeroes for various figures/timeframes to start cumulative counts
def addZeroes(theme, themeCts, zeroes):
    for type in themeCts:
        for tf in themeCts[type]:
            ## Theme counts for various themes for given timeframe
            tc = themeCts[type][tf]

            if theme not in tc:
                tc[theme] = list(zeroes[type][tf])

    return

## For gathering counts associated with a tweet (e.g. favorites or retweets)
#
#  @param index int
#   the column index of the count to be gathered
#
#  @param row list
#   row for tweet from source data
#
#  @return count as integer
def getCount(index, row):
    ## Count from tweet
    ct = row[index]

    if ct == '':
        ct = 0

    return int(ct)

## Initializes count list for various themes at various timeframes
#
#  @param themeCts dict
#   dictionary of count lists for various themes and timeframes
#
#  @param theme tuple
#   theme count list to be initialized
def initThemeCounts(themeCts, theme):
    for type in themeCts:
        for tf in themeCts[type]:
            themeCts[type][tf][theme] = [0]

    return

## Initializes zeroes padding for various themes at various timeframes
#
#  @param themeCts dict
#   dictionary of count lists for various themes and timeframes
def initZeroes(themeCts):
    ## Pad counts with zeroes when theme / message type has not appeared yet
    zeroes = {}

    for type in themeCts:
        zeroes[type] = {}

        for tf in themeCts[type]:
            zeroes[type][tf] = [0]

    return zeroes

## Calculates updated counts for all tweets for latest timeframe
#
#  @param ct dict
#   the amount to update the count depending on what type of figure is updated
#
#  @param cum bool
#   whether count update is cumulative
#
#  @param new dict
#   whether latest timeframe is a new time
#
#  @param themeCts dict
#   stores various counts for various timeframes
#
#  @param zeroes dict
#   lists of zeroes for various figures/timeframes to start cumulative counts
def updateAllTweetsCount(ct, cum, new, themeCts, zeroes):
    for type in themeCts:
        for tf in themeCts[type]:
            ## Count of all tweets over time
            twCts = themeCts[type][tf][('ALL', 'ALL')]

            if new[tf]:
                zeroes[type][tf].append(0)

                if cum:
                    twCts.append(twCts[-1])
                else:
                    twCts.append(0)

            twCts[-1] += ct[type]

    return

## Calculates updated counts for latest timeframe
#
#  @param ct dict
#   the amount to update the count depending on what type of figure is updated
#
#  @param cum bool
#   whether count update is cumulative
#
#  @param new dict
#   whether latest timeframe is a new time
#
#  @param rowThemes list
#   list of theme-type, theme-name pairs that identify theme / message type
#
#  @param test bool
#   whether theme is present for the tweet
#
#  @param theme tuple
#   theme-type, theme-name pair that identifies theme / message type
#
#  @param themeCts dict
#   stores various counts for various timeframes
def updateCounts(ct, cum, new, rowThemes, test, theme, themeCts):
    for type in themeCts:
        for tf in themeCts[type]:
            ## Count of theme / message type over time
            tc = themeCts[type][tf][theme]

            if new[tf]:
                if cum:
                    tc.append(tc[-1])
                else:
                    tc.append(0)

            if len(rowThemes) == 1:
                if test:
                    tc[-1] += ct[type]
            else:
                for st in rowThemes:
                    if theme == st:
                        tc[-1] += ct[type]

    return

## Writes various files for counts, percent mixes, and ratios
#
#  @param cum bool
#   whether count update is cumulative
#
#  @param themeCts dict
#   stores various counts for various timeframes
#
#  @param times dict
#   dates and/or times of tweets for various timeframes
def writeFiles(cum, themeCts, times):
    ## Additon to filename for cumulative counts
    cTxt = ''

    if cum:
        cTxt = 'Cum'

    ## Filenames for count timeline data
    tlCtFnames = {'Fav': {'DT': 'TL_Favorites_' + cTxt + 'Ct.csv',
                          'Mo': 'Mo_Favorites_' + cTxt + 'Ct.csv'},
                  'RT': {'DT': 'TL_Retweets_' + cTxt + 'Ct.csv',
                         'Mo': 'Mo_Retweets_' + cTxt + 'Ct.csv'},
                  'Tw': {'DT': 'TL_Tweets_' + cTxt + 'Ct.csv',
                         'Mo': 'Mo_Tweets_' + cTxt + 'Ct.csv'}}

    ## Filenames for proportion to total tweets data
    tlPrFnames = {'Fav': {'DT': 'TL_Favorites_' + cTxt + 'PctMix.csv',
                          'Mo': 'Mo_Favorites_' + cTxt + 'PctMix.csv'},
                  'RT': {'DT': 'TL_Retweets_' + cTxt + 'PctMix.csv',
                         'Mo': 'Mo_Retweets_' + cTxt + 'PctMix.csv'},
                  'Tw': {'DT': 'TL_Tweets_' + cTxt + 'PctMix.csv',
                         'Mo': 'Mo_Tweets_' + cTxt + 'PctMix.csv'}}

    ## Filenames for ratio to tweet count data
    tlRatioFnames = {'Fav': {'DT': 'TL_Favs2Tweets_' + cTxt + 'Ratio.csv',
                             'Mo': 'Mo_Favs2Tweets_' + cTxt + 'Ratio.csv'},
                     'RT': {'DT': 'TL_RTtoTweets_' + cTxt + 'Ratio.csv',
                            'Mo': 'Mo_RTtoTweets_' + cTxt + 'Ratio.csv'}}

    ## Filenames for monthly growth rates of ratios
    ratioGrowthFnames = {'Fav': 'Mo_Favs2Tweets_' + cTxt + 'RatioGrowth.csv',
                         'RT': 'Mo_RTtoTweets_' + cTxt + 'RatioGrowth.csv'}

    ## Cumulative counts for various timeframes
    tlCts = {}

    for type in themeCts:
        tlCts[type] = {}

        for tf in themeCts[type]:
            ## Range for iterating through lists at each date/time
            dateRange = range(1, len(times[tf]) + 1)

            ## Count timeline list for CSV file
            timelineCt = [['Type', 'Name'] + times[tf]]

            ## Proportion timeline list for CSV file
            timelinePr = list(timelineCt)

            ## Counts of various themes / message types
            tcLists = themeCts[type][tf]

            for theme in tcLists:
                ## Count timeline list for specific theme / message type
                tc = tcLists[theme]

                ## Theme tuple as list
                themeList = list(theme)

                timelineCt.append(themeList + tc[1:])

                ## Proportion timeline for theme / message type
                themePrs = []

                for i in dateRange:
                    if tc[i] == 0:
                        themePrs.append(0)
                    else:
                        themePrs.append(
                            tc[i] / float(tcLists[('ALL', 'ALL')][i]))

                timelinePr.append(themeList + themePrs)

            tlCts[type][tf] = timelineCt

            ## To write count timeline data
            tlCtCSV = csv.writer(open(tlCtFnames[type][tf], 'wb',
                                      buffering = 0))

            ## To write proportion timeline data
            tlPrCSV = csv.writer(open(tlPrFnames[type][tf], 'wb',
                                      buffering = 0))

            tlCtCSV.writerows(timelineCt)
            tlPrCSV.writerows(timelinePr)

    for type in tlRatioFnames:
        for tf in themeCts[type]:
            ## Counts for various themes
            tc = tlCts[type][tf]

            ## Test for whether timeframe is month
            moTest = tf == 'Mo'

            if moTest:
                ## Ratio growth timeline list for CSV file
                timelineGrowth = [tc[0]]

            ## Ratio timeline list for CSV file
            timelineRatio = [tc[0]]

            ## Range for themes / message types
            themeRng = range(1, len(tc))

            for i in themeRng:
                if moTest:
                    ## Ratio growth timeline for theme / message type
                    themeGrowth = tc[i][:2]

                    ## Previous ratio for growth calculations
                    prevRatio = 0.0

                ## Ratio timeline for theme / message type
                themeRatio = tc[i][:2]

                ## Range for counts of theme / message type
                ctRng = range(2, len(tc[i]))

                for j in ctRng:
                    ## Ratio for one theme / message type at one time
                    ratio = float(tlCts['Tw'][tf][i][j])

                    if ratio != 0.0:
                        ratio = tc[i][j] / ratio

                    themeRatio.append(ratio)

                    if moTest:
                        ## Growth rate for one theme / message type at one time
                        growth = prevRatio

                        if growth != 0.0:
                            growth = (ratio - prevRatio) / prevRatio

                        themeGrowth.append(growth)
                        prevRatio = ratio

                timelineRatio.append(themeRatio)

                if moTest:
                    timelineGrowth.append(themeGrowth)

            ## To write ratio timeline data
            tlRatioCSV = csv.writer(open(tlRatioFnames[type][tf], 'wb',
                                         buffering = 0))

            tlRatioCSV.writerows(timelineRatio)

            if moTest:
                ## To write ratio growth timeline data
                tlGrowthCSV = csv.writer(open(ratioGrowthFnames[type],
                                              'wb', buffering = 0))

                tlGrowthCSV.writerows(timelineGrowth)

    return


def main():
    print 'Usage Note:'
    print 'Ensure DateRoot column is sorted in chronological order'

    ## Filepath of CSV source file
    [source] = getSysArgs.usage(['themeTimeline.py',
                                 '<source_CSV_filepath>'])[1:]

    ## Open source CSV file
    source = csv.reader(open(source, 'rU'))

    ## Names of binaries/composites
    binaries = []

    ## Table column names
    colNames = source.next()

    ## Cumulative counts for all tweets
    allCt = {('ALL', 'ALL'): [0]}

    ## Timeframes for counts
    tFrames = {'DT': dcp(allCt), 'Mo': dcp(allCt)}

    ## Non-cumulative count types
    themeCts = {'Fav': {'Mo': dcp(allCt)}, 'RT': {'Mo': dcp(allCt)},
                'Tw': {'Mo': dcp(allCt)}}

    ## Cumulative count types
    themeCumCts = {'Fav': dcp(tFrames), 'RT': dcp(tFrames), 'Tw': dcp(tFrames)}

    for name in colNames:
        ## Lowercased column name
        nameLC = name.strip().lower()

        if nameLC.find('binary') != -1:
            binaries.append(name)
            name = ('binary/composite', name)
            initThemeCounts(themeCts, name)
            initThemeCounts(themeCumCts, name)

    ## Index of favorite count column
    favI = colNames.index('Favorite Count')

    ## Names of message types
    msgTypes = []

    ## Index of message type column
    mtI = colNames.index('Message Type')

    ## Index of retweet count column
    rtI = colNames.index('Retweet Count')

    ## Names of sub-themes
    subThemes = []

    ## Column indices for sub-themes
    themeCols = (colNames.index('Theme 1'), colNames.index('Theme 2'),
                 colNames.index('Theme 3'), colNames.index('Theme 4'))

    ## Dates and/or times of tweets for various timeframes
    times = {}

    for tf in tFrames:
        times[tf] = []

    ## Pad counts with zeroes when theme / message type has not appeared yet
    zeroes = initZeroes(themeCts)

    ## Pad cumulative counts with zeroes
    zeroesCum = initZeroes(themeCumCts)

    for row in source:
        ## Timestamp of tweet
        dt = parse(row[colNames.index('DateRoot')])

        ## To update if nearest minute is start of next hour
        hr = dt.hour

        ## To round timestamp to the nearest minute
        min = dt.minute

        if dt.second >= 30:
            min += 1

        if min == 60:
            hr += 1
            min = 0

        ## Month of tweet
        month = dt.date().replace(day = 1).isoformat()

        dt = dt.replace(hour = hr, minute = min, second = 0,
                        microsecond = 0).isoformat(' ')

        ## For operations sensitive to whether a new date/time is in review
        new = {}

        ## Date and/or times of various timeframes
        time = {'DT': dt, 'Mo': month}

        for tf in tFrames:
            new[tf] = time[tf] not in times[tf]

            if new[tf]:
                times[tf].append(time[tf])

        ## Counts for all types
        ct = {'Fav': getCount(favI, row), 'RT': getCount(rtI, row), 'Tw': 1}

        for binary in binaries:                    
            ## Test whether binary should have counts updated
            binTest = int(row[colNames.index(binary)]) > 0

            binary = ('binary/composite', binary)
            updateCounts(ct, False, new, [binary], binTest, binary, themeCts)
            updateCounts(ct, True, new, [binary], binTest, binary, themeCumCts)

        ## Message Type being reviewed
        msgType = row[mtI].strip().lower().title()

        if msgType not in msgTypes:
            msgTypes.append(msgType)

        msgType = ('message type', msgType)
        addZeroes(msgType, themeCts, zeroes)
        addZeroes(msgType, themeCumCts, zeroesCum)

        for mt in msgTypes:
            ## Test whether message type should have counts updated
            mtTest = mt == msgType[1]

            mt = ('message type', mt)
            updateCounts(ct, False, new, [mt], mtTest, mt, themeCts)
            updateCounts(ct, True, new, [mt], mtTest, mt, themeCumCts)

        ## Sub-themes for row
        rowThemes = []

        for i in themeCols:
            ## One sub-theme for tweet being reviewed
            theme = row[i].strip().lower().title()

            if theme != '' and theme not in rowThemes:
                rowThemes.append(theme)

                if theme not in subThemes:
                    subThemes.append(theme)

                theme = ('sub-theme', theme)
                addZeroes(theme, themeCts, zeroes)
                addZeroes(theme, themeCumCts, zeroesCum)

        for st in subThemes:
            st = ('sub-theme', st)
            updateCounts(ct, False, new, rowThemes, None, st, themeCts)
            updateCounts(ct, True, new, rowThemes, None, st, themeCumCts)

        updateAllTweetsCount(ct, False, new, themeCts, zeroes)
        updateAllTweetsCount(ct, True, new, themeCumCts, zeroesCum)

    writeFiles(False, themeCts, times)
    writeFiles(True, themeCumCts, times)

    return

if __name__ == '__main__':
    main()
