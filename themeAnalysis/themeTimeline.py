from copy import deepcopy as dcp
from dateutil.parser import parse

import csv, getSysArgs


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

        ## Tweet's favorite count
        favCt = row[favI]

        if favCt == '':
            favCt = 0

        favCt = int(favCt)

        ## Tweet's retweet count
        rtCt = row[rtI]

        if rtCt == '':
            rtCt = 0

        rtCt = int(rtCt)

        ## Counts for all types
        ct = {'Fav': favCt, 'RT': rtCt, 'Tw': 1}

        for binary in binaries:
            ## Test for whether binary/composite is attributed to tweet
            binTest = int(row[colNames.index(binary)]) > 0

            binary = ('binary/composite', binary)

            for type in themeCts:
                for tf in tFrames:
                    ## List of counts for the binary/composite
                    binCts = themeCts[type][tf][binary]

                    if new[tf]:  #create count for new timeframe 
                        binCts.append(binCts[-1])

                    if binTest:
                        binCts[-1] += ct[type]

        ## Message Type being reviewed
        msgType = row[mtI].strip().lower().title()

        if msgType not in msgTypes:
            msgTypes.append(msgType)

        msgType = ('message type', msgType)

        for type in themeCts:
            for tf in tFrames:
                ## Theme count for given timeframe
                tc = themeCts[type][tf]

                if msgType not in tc:
                    tc[msgType] = list(zeroes[type][tf])

        for mt in msgTypes:
            ## Test for whether message type is attributed to tweet
            mtTest = mt == msgType[1]

            mt = ('message type', mt)

            for type in themeCts:
                for tf in tFrames:
                    ## Message type counts over time
                    mtCts = themeCts[type][tf][mt]

                    if new[tf]:
                        mtCts.append(mtCts[-1])

                    if mtTest:
                        mtCts[-1] += ct[type]

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

                for type in themeCts:
                    for tf in tFrames:
                        ## Theme count for given timeframe
                        tc = themeCts[type][tf]

                        if theme not in tc:
                            tc[theme] = list(zeroes[type][tf])

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

    for type in themeCts:
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

            ## To write count timeline data
            tlCtCSV = csv.writer(open(tlCtFnames[type][tf], 'wb',
                                      buffering = 0))

            ## To write proportion timeline data
            tlPrCSV = csv.writer(open(tlPrFnames[type][tf], 'wb',
                                      buffering = 0))

            tlCtCSV.writerows(timelineCt)
            tlPrCSV.writerows(timelinePr)

    return

if __name__ == '__main__':
    main()
