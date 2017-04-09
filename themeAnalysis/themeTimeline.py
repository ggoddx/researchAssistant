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

    ## Cumulative counts for various timeframes
    themeCts = {'DT': {('ALL', 'ALL'): [0]}, 'Mo': {('ALL', 'ALL'): [0]}}

    ## Cumulative favorite counts for various timeframes
    themeFavCts = {'DT': {('ALL', 'ALL'): [0]}, 'Mo': {('ALL', 'ALL'): [0]}}

    ## Cumulative retweet counts for various timeframes
    themeRTcts = {'DT': {('ALL', 'ALL'): [0]}, 'Mo': {('ALL', 'ALL'): [0]}}

    for name in colNames:
        ## Lowercased column name
        nameLC = name.strip().lower()

        if nameLC.find('binary') != -1:
            binaries.append(name)
            name = ('binary/composite', name)

            for tf in themeCts:
                themeCts[tf][name] = [0]
                themeRTcts[tf][name] = [0]
                themeFavCts[tf][name] = [0]

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
    times = {'DT': [], 'Mo': []}

    ## Pad counts with zeroes when theme / message type has not appeared yet
    zeroes = {'DT': [0], 'Mo': [0]}

    ## Zero pad for favorites
    zeroesFav = {'DT': [0], 'Mo': [0]}

    ## Zero pad for retweets
    zeroesRT = {'DT': [0], 'Mo': [0]}

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
        new = {'DT': None, 'Mo': None}

        ## Date and/or times of various timeframes
        time = {'DT': dt, 'Mo': month}

        for tf in themeCts:
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

        for binary in binaries:
            ## Test for whether binary/composite is attributed to tweet
            binTest = int(row[colNames.index(binary)]) > 0

            binary = ('binary/composite', binary)

            for tf in themeCts:
                ## List of counts for binary in theme / message type count dict
                binCts = themeCts[tf][binary]

                ## List of favorite counts for the binary/composite
                binFavCts = themeFavCts[tf][binary]

                ## List of rewtweet counts for the binary/composite
                binRTcts = themeRTcts[tf][binary]

                if new[tf]:  #create count for new timeframe
                    binCts.append(binCts[-1])
                    binFavCts.append(binFavCts[-1])
                    binRTcts.append(binRTcts[-1])

                if binTest:
                    binCts[-1] += 1
                    binFavCts[-1] += favCt
                    binRTcts[-1] += rtCt

        ## Message Type being reviewed
        msgType = row[mtI].strip().lower().title()

        if msgType not in msgTypes:
            msgTypes.append(msgType)

        msgType = ('message type', msgType)

        for tf in themeCts:
            ## Theme count for given timeframe
            tc = themeCts[tf]

            ## Favorite count for given timeframe
            tFavCt = themeFavCts[tf]

            ## Retweet count for given timeframe
            tRTc = themeRTcts[tf]

            if msgType not in tc:
                tc[msgType] = list(zeroes[tf])

            if msgType not in tFavCt:
                tFavCt[msgType] = list(zeroesFav[tf])

            if msgType not in tRTc:
                tRTc[msgType] = list(zeroesRT[tf])

        for mt in msgTypes:
            ## Test for whether message type is attributed to tweet
            mtTest = mt == msgType[1]

            mt = ('message type', mt)

            for tf in themeCts:
                ## Message type counts' list in theme / message type count dict
                msgTypeCts = themeCts[tf][mt]

                ## Favorite count list for message type
                msgTypeFavCts = themeFavCts[tf][mt]

                ## Retweet count list for message type
                msgTypeRTcts = themeRTcts[tf][mt]

                if new[tf]:
                    msgTypeCts.append(msgTypeCts[-1])
                    msgTypeFavCts.append(msgTypeFavCts[-1])
                    msgTypeRTcts.append(msgTypeRTcts[-1])

                if mtTest:
                    msgTypeCts[-1] += 1
                    msgTypeFavCts[-1] += favCt
                    msgTypeRTcts[-1] += rtCt

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

                for tf in themeCts:
                    ## Theme count for given timeframe
                    tc = themeCts[tf]

                    ## Favorite count for given timeframe
                    tFavCt = themeFavCts[tf]

                    ## Retweet count for given timeframe
                    tRTc = themeRTcts[tf]

                    if theme not in tc:
                        tc[theme] = list(zeroes[tf])

                    if theme not in tFavCt:
                        tFavCt[theme] = list(zeroesFav[tf])

                    if theme not in tRTc:
                        tRTc[theme] = list(zeroesRT[tf])

        for st in subThemes:
            st = ('sub-theme', st)

            for tf in themeCts:
                ## Sub-theme counts' list in theme / message type count dict
                subThemeCts = themeCts[tf][st]

                ## Favorite count list for sub-theme
                subThemeFavCts = themeFavCts[tf][st]

                ## Retweet count list for sub-theme
                subThemeRTcts = themeRTcts[tf][st]

                if new[tf]:
                    subThemeCts.append(subThemeCts[-1])
                    subThemeFavCts.append(subThemeFavCts[-1])
                    subThemeRTcts.append(subThemeRTcts[-1])

                for theme in rowThemes:
                    if st[1] == theme:
                        subThemeCts[-1] += 1
                        subThemeFavCts[-1] += favCt
                        subThemeRTcts[-1] += rtCt

        for tf in themeCts:
            ## Count of tweet over timeframe
            tweetCts = themeCts[tf][('ALL', 'ALL')]

            ## Favorite count over timeframe
            tweetFavCts = themeFavCts[tf][('ALL', 'ALL')]

            ## Retweet count over timeframe
            tweetRTcts = themeRTcts[tf][('ALL', 'ALL')]

            if new[tf]:
                zeroes[tf].append(0)
                zeroesFav[tf].append(0)
                zeroesRT[tf].append(0)
                tweetCts.append(tweetCts[-1])
                tweetFavCts.append(tweetFavCts[-1])
                tweetRTcts.append(tweetRTcts[-1])

            tweetCts[-1] += 1
            tweetFavCts[-1] += favCt
            tweetRTcts[-1] += rtCt

    ## Filename for count timeline data at various timeframes
    tlCtFname = {'DT': 'themeCountTimeline.csv', 'Mo': 'themeCountByMonth.csv'}

    ## Filename for proportion timeline data at various timeframes
    tlPrFname = {'DT': 'themePercentTimeline.csv',
                 'Mo': 'themePercentByMonth.csv'}

    ## Filename for favorite count timeline data at various timeframes
    tlFavFname = {'DT': 'themeFavTimeline.csv', 'Mo': 'themeFavByMonth.csv'}

    ## Filename for retweet count timeline data at various timeframes
    tlRTfname = {'DT': 'themeRTtimeline.csv', 'Mo': 'themeRTbyMonth.csv'}

    for tf in themeCts:
        ## Range for iterating through lists at each date/time
        dateRange = range(1, len(times[tf]) + 1)

        ## Count timeline list for CSV file
        timelineCt = [['Type', 'Name'] + times[tf]]

        ## Proportion timeline list for CSV file
        timelinePr = list(timelineCt)

        ## Favorite count timeline list for CSV file
        timelineFav = list(timelineCt)

        ## Retweet count timeline list for CSV file
        timelineRT = list(timelineCt)

        for theme in themeCts[tf]:
            ## Count timeline list for specific theme / message type
            themeCount = themeCts[tf][theme]

            ## Theme tuple as list
            themeList = list(theme)

            timelineCt.append(themeList + themeCount[1:])

            ## Proportion timeline for theme / message type
            themePrs = []

            for i in dateRange:
                themePrs.append(
                    themeCount[i] / float(themeCts[tf][('ALL', 'ALL')][i]))

            timelinePr.append(themeList + themePrs)

        for theme in themeFavCts[tf]:
            timelineFav.append(list(theme) + themeFavCts[tf][theme][1:])

        for theme in themeRTcts[tf]:
            timelineRT.append(list(theme) + themeRTcts[tf][theme][1:])

        ## To write count timeline data
        tlCtCSV = csv.writer(open(tlCtFname[tf], 'wb', buffering = 0))

        ## To write proportion timeline data
        tlPrCSV = csv.writer(open(tlPrFname[tf], 'wb', buffering = 0))

        ## To write favorite count timeline data
        tlFavCSV = csv.writer(open(tlFavFname[tf], 'wb', buffering = 0))

        ## To write retweet count timeline data
        tlRTcsv = csv.writer(open(tlRTfname[tf], 'wb', buffering = 0))

        tlCtCSV.writerows(timelineCt)
        tlPrCSV.writerows(timelinePr)
        tlFavCSV.writerows(timelineFav)
        tlRTcsv.writerows(timelineRT)

    return

if __name__ == '__main__':
    main()
