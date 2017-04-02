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

    ## Table column names
    colNames = source.next()

    ## Names of binaries/composites
    binaries = []

    ## Cumulative counts of themes / message types over time
    themeDTcts = {('ALL', 'ALL'): [0]}

    ## Cumulative counts of themes / message types by month
    themeMoCts = {('ALL', 'ALL'): [0]}

    ## Cumulative counts for various timeframes
    themeCts = {'DT': themeDTcts, 'Mo': themeMoCts}

    for name in colNames:
        ## Lowercased column name
        nameLC = name.strip().lower()

        if nameLC.find('binary') != -1:
            binaries.append(name)

            for tf in themeCts:
                themeCts[tf][('binary/composite', name)] = [0]

    ## Dates or tweets
    dates = []

    ## Month of tweets
    months = []

    ## Dates and/or times of tweets for various timeframes
    times = {'DT': dates, 'Mo': months}

    ## Names of message types
    msgTypes = []

    ## Names of sub-themes
    subThemes = []

    ## Column indices for sub-themes
    themeCols = (colNames.index('Theme 1'), colNames.index('Theme 2'),
                 colNames.index('Theme 3'), colNames.index('Theme 4'))

    zeroes = {'DT': [0], 'Mo': [0]}

    for row in source:
        ## Timestamp of tweet
        dt = parse(row[colNames.index('DateRoot')])

        ## To round timestamp to the nearest minute
        min = dt.minute

        ## If nearest minute is start of next hour
        hr = dt.hour

        if dt.second >= 30:
            min += 1

        if min == 60:
            hr += 1
            min = 0

        ## Month of tweet
        month = dt.date().replace(day = 1).isoformat()

        dt = dt.replace(hour = hr, minute = min, second = 0,
                        microsecond = 0).isoformat(' ')

        ## Date and/or times of various timeframes
        time = {'DT': dt, 'Mo': month}

        ## For operations sensitive to whether a new date/time is in review
        new = {'DT': None, 'Mo': None}

        for tf in themeCts:
            new[tf] = time[tf] not in times[tf]

            if new[tf]:
                times[tf].append(time[tf])

        for binary in binaries:
            for tf in themeCts:
                ## List of counts for binary in theme / message type count dict
                binCts = themeCts[tf][('binary/composite', binary)]

                if new[tf]:
                    binCts.append(binCts[-1])  #tweet count for new timeframe

                if int(row[colNames.index(binary)]) > 0:
                    binCts[-1] += 1

        ## Message Type being reviewed
        msgType = row[colNames.index('Message Type')].strip().lower().title()

        if msgType not in msgTypes:
            msgTypes.append(msgType)

        msgType = ('message type', msgType)

        for tf in themeCts:
            if msgType not in themeCts[tf]:
                themeCts[tf][msgType] = list(zeroes[tf])

        for mt in msgTypes:
            for tf in themeCts:
                ## Message type counts' list in theme / message type count dict
                msgTypeCts = themeCts[tf][('message type', mt)]

                if new[tf]:
                    msgTypeCts.append(msgTypeCts[-1])

                if mt == msgType[1]:
                    msgTypeCts[-1] += 1

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
                    if theme not in themeCts[tf]:
                        themeCts[tf][theme] = list(zeroes[tf])

        for st in subThemes:
            for tf in themeCts:
                ## Sub-theme counts' list in theme / message type count dict
                subThemeCts = themeCts[tf][('sub-theme', st)]

                if new[tf]:
                    subThemeCts.append(subThemeCts[-1])

                for theme in rowThemes:
                    if st == theme:
                        subThemeCts[-1] += 1

        for tf in themeCts:
            ## Count of tweet over timeframe
            tweetCts = themeCts[tf][('ALL', 'ALL')]

            if new[tf]:
                zeroes[tf].append(0)
                tweetCts.append(tweetCts[-1])

            tweetCts[-1] += 1

    ## Filename for count timeline data at various timeframes
    tlCtFname = {'DT': 'themeCountTimeline.csv', 'Mo': 'themeCountByMonth.csv'}

    ## Filename for proportion timeline data at various timeframes
    tlPrFname = {'DT': 'themePercentTimeline.csv',
                 'Mo': 'themePercentByMonth.csv'}

    for tf in themeCts:
        ## Range for iterating through lists at each date/time
        dateRange = range(1, len(times[tf]) + 1)

        ## Count timeline list for CSV file
        timelineCt = [['Type', 'Name'] + times[tf]]

        ## Proportion timeline list for CSV file
        timelinePr = list(timelineCt)

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

        ## To write count timeline data
        tlCtCSV = csv.writer(open(tlCtFname[tf], 'wb', buffering = 0))

        ## To write proportion timeline data
        tlPrCSV = csv.writer(open(tlPrFname[tf], 'wb', buffering = 0))

        tlCtCSV.writerows(timelineCt)
        tlPrCSV.writerows(timelinePr)

    return

if __name__ == '__main__':
    main()
