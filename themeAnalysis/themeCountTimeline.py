from dateutil.parser import parse

import csv, getSysArgs


def main():
    print 'Usage Note:'
    print 'Ensure DateRoot column is sorted in chronological order'

    ## Filepath of CSV source file
    [source] = getSysArgs.usage(['themeCountTimeline.py',
                                 '<source_CSV_filepath>'])[1:]

    ## Open source CSV file
    source = csv.reader(open(source, 'rU'))

    ## Table column names
    colNames = source.next()

    ## Names of binaries/composites
    binaries = []

    ## Cumulative counts of themes / message types over time
    themeCts = {('ALL', 'ALL'): [0]}

    for name in colNames:
        ## Lowercased column name
        nameLC = name.strip().lower()

        if nameLC.find('binary') != -1:
            binaries.append(name)
            themeCts[('binary/composite', name)] = [0]

    ## Dates or tweets
    dates = []

    ## Names of message types
    msgTypes = []

    ## Names of sub-themes
    subThemes = []

    ## Column indices for sub-themes
    themeCols = (colNames.index('Theme 1'), colNames.index('Theme 2'),
                 colNames.index('Theme 3'), colNames.index('Theme 4'))

    ## To pad rows with zeroes when theme / message type is yet to be present
    zeroes = [0]

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

        dt = dt.replace(hour = hr, minute = min,
                        second = 0, microsecond = 0).isoformat(' ')

        ## For operations sensitive to whether a new date & time is in review
        newDT = dt not in dates

        if newDT:
            dates.append(dt)

        for binary in binaries:
            ## List of counts for binary in theme / message type count dict
            binCts = themeCts[('binary/composite', binary)]

            if newDT:
                binCts.append(binCts[-1])  #tweet count for new date & time

            if int(row[colNames.index(binary)]) > 0:
                binCts[-1] += 1

        ## Message Type being reviewed
        msgType = row[colNames.index('Message Type')].strip().lower().title()

        if msgType not in msgTypes:
            msgTypes.append(msgType)

        msgType = ('message type', msgType)

        if msgType not in themeCts:
            themeCts[msgType] = list(zeroes)

        for mt in msgTypes:
            ## List of message type counts in theme / message type count dict
            msgTypeCts = themeCts[('message type', mt)]

            if newDT:
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

                if theme not in themeCts:
                    themeCts[theme] = list(zeroes)

        for st in subThemes:
            ## List of sub-themes counts in theme / message type count dict
            subThemeCts = themeCts[('sub-theme', st)]

            if newDT:
                subThemeCts.append(subThemeCts[-1])

            for theme in rowThemes:
                if st == theme:
                    subThemeCts[-1] += 1

        ## Count of tweets over time
        tweetCts = themeCts[('ALL', 'ALL')]

        if newDT:
            zeroes.append(0)
            tweetCts.append(tweetCts[-1])

        tweetCts[-1] += 1

    ## Timeline list for CSV file
    timeline = [['Type', 'Name'] + dates]

    for theme in themeCts:
        timeline.append(list(theme) + themeCts[theme][1:])

    ## To write timeline data
    tlCSV = csv.writer(open('themeCountTimeline.csv', 'wb', buffering = 0))

    tlCSV.writerows(timeline)

    return

if __name__ == '__main__':
    main()
