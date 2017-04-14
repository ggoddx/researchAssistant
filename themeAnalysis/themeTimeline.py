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

## Calculates updated counts for latest timeframe
#
#  @param ct dict
#   the amount to update the count depending on what type of figure is updated
#
#  @param new dict
#   whether latest timeframe is a new time
#
#  @param test bool
#   whether theme is present for the tweet
#
#  @param theme tuple
#   theme-type, theme-name pair that identifies theme / message type
#
#  @param themeCts dict
#   stores various counts for various timeframes
def updateCounts(ct, new, test, theme, themeCts):
    for type in themeCts:
        for tf in themeCts[type]:
            ## Cumulative count of theme / message type over time
            tc = themeCts[type][tf][theme]

            if new[tf]:
                tc.append(tc[-1])

            if test:
                tc[-1] += ct[type]

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

    ## Count types
    themeCts = {'Fav': dcp(tFrames), 'RT': dcp(tFrames), 'Tw': dcp(tFrames)}

    for name in colNames:
        ## Lowercased column name
        nameLC = name.strip().lower()

        if nameLC.find('binary') != -1:
            binaries.append(name)
            name = ('binary/composite', name)

            for type in themeCts:
                for tf in tFrames:
                    themeCts[type][tf][name] = [0]

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
    zeroes = {}

    for type in themeCts:
        zeroes[type] = {}

        for tf in tFrames:
            zeroes[type][tf] = [0]

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
            updateCounts(ct, new, int(row[colNames.index(binary)]) > 0,
                         ('binary/composite', binary), themeCts)

        ## Message Type being reviewed
        msgType = row[mtI].strip().lower().title()

        if msgType not in msgTypes:
            msgTypes.append(msgType)

        addZeroes(('message type', msgType), themeCts, zeroes)

        for mt in msgTypes:
            updateCounts(ct, new, mt == msgType, ('message type', mt),
                         themeCts)

        ## Sub-themes for row
        rowThemes = []

        for i in themeCols:
            ## One sub-theme for tweet being reviewed
            theme = row[i].strip().lower().title()

            if theme != '' and theme not in rowThemes:
                rowThemes.append(theme)

                if theme not in subThemes:
                    subThemes.append(theme)

                addZeroes(('sub-theme', theme), themeCts, zeroes)

        for st in subThemes:
            st = ('sub-theme', st)

            for type in themeCts:
                for tf in tFrames:
                    ## Sub-theme counts over time
                    stCts = themeCts[type][tf][st]

                    if new[tf]:
                        stCts.append(stCts[-1])

                    for theme in rowThemes:
                        if st[1] == theme:
                            stCts[-1] += ct[type]

        for type in themeCts:
            for tf in tFrames:
                ## Count of all tweets over time
                twCts = themeCts[type][tf][('ALL', 'ALL')]

                if new[tf]:
                    zeroes[type][tf].append(0)
                    twCts.append(twCts[-1])

                twCts[-1] += ct[type]

    ## Filenames for count timeline data
    tlCtFnames = {'Fav': {'DT': 'allThemesTL_Favorites_Ct.csv',
                          'Mo': 'allThemesMo_Favorites_Ct.csv'},
                  'RT': {'DT': 'allThemesTL_Retweets_Ct.csv',
                         'Mo': 'allThemesMo_Retweets_Ct.csv'},
                  'Tw': {'DT': 'allThemesTL_Tweets_Ct.csv',
                         'Mo': 'allThemesMo_Tweets_Ct.csv'}}

    ## Filenames for proportion to total tweets data
    tlPrFnames = {'Fav': {'DT': 'allThemesTL_Favorites_PctMix.csv',
                          'Mo': 'allThemesMo_Favorites_PctMix.csv'},
                  'RT': {'DT': 'allThemesTL_Retweets_PctMix.csv',
                         'Mo': 'allThemesMo_Retweets_PctMix.csv'},
                  'Tw': {'DT': 'allThemesTL_Tweets_PctMix.csv',
                         'Mo': 'allThemesMo_Tweets_PctMix.csv'}}

    ## Filenames for ratio to tweet count data
    tlRatioFnames = {'Fav': {'DT': 'allThemesTL_Favs2Tweets_Ratio.csv',
                             'Mo': 'allThemesMo_Favs2Tweets_Ratio.csv'},
                     'RT': {'DT': 'allThemesTL_RTtoTweets_Ratio.csv',
                            'Mo': 'allThemesMo_RTtoTweets_Ratio.csv'}}

    ## Filenames for monthly growth rates of ratios
    ratioGrowthFnames = {'Fav': 'allThemesMo_Favs2Tweets_RatioGrowth.csv',
                         'RT': 'allThemesMo_RTtoTweets_RatioGrowth.csv'}

    ## Cumulative counts for various timeframes
    tlCts = {}

    for type in themeCts:
        tlCts[type] = {}

        for tf in tFrames:
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
                    themePrs.append(tc[i] / float(tcLists[('ALL', 'ALL')][i]))

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
        for tf in tFrames:
            ## Counts for various themes
            tc = tlCts[type][tf]

            ## Ratio timeline list for CSV file
            timelineRatio = [tc[0]]

            ## Range for themes / message types
            themeRng = range(1, len(tc))

            for i in themeRng:
                ## Ratio timeline for theme / message type
                themeRatio = tc[i][:2]

                ## Range for counts of theme / message type
                ctRng = range(2, len(tc[i]))

                for j in ctRng:
                    ## Ratio for one theme / message type for one time
                    ratio = float(tlCts['Tw'][tf][i][j])

                    if ratio != 0.0:
                        ratio = tc[i][j] / ratio

                    themeRatio.append(ratio)

                timelineRatio.append(themeRatio)

            ## To write ratio timeline data
            tlRatioCSV = csv.writer(open(tlRatioFnames[type][tf], 'wb',
                                         buffering = 0))

            tlRatioCSV.writerows(timelineRatio)

    return

if __name__ == '__main__':
    main()
