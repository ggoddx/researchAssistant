import csv, getSysArgs


def main():
    ## CSV file of tweets and data
    [fName] = getSysArgs.usage(['multiTheme.py',
                                '<tweetdata_CSV_file_path>'])[1:]

    ## Open tweet data CSV file
    data = csv.reader(open(fName, 'rU'))

    ## Table column names
    colNames = data.next()

    ## Column indices for the sub-themes
    themeIs = (colNames.index('Theme 1'), colNames.index('Theme 2'),
               colNames.index('Theme 3'), colNames.index('Theme 4'))

    ## Names of sub-themes
    subThemes = []

    ## Sub-theme combinations counts
    multiThemes = {}

    for row in data:
        ## Sub-Themes for row
        rowThemes = []

        for i in themeIs:
            ## One of the sub-themes in the row
            theme = row[i].lower().strip()

            if theme == '':
                continue

            if theme not in subThemes:
                subThemes.append(theme)

            if theme not in rowThemes:
                rowThemes.append(theme)

        rowThemes.sort()
        rowThemes = tuple(rowThemes)

        if rowThemes not in multiThemes:
            multiThemes[rowThemes] = 0

        multiThemes[rowThemes] += 1

    ## To make a list out of the multiThemes dictionary
    themeCt = []

    for combo in multiThemes:
        themeCt.append([combo, multiThemes[combo]])

    ## File to write theme-combination counts
    themeCtCSV = csv.writer(open('subThemeComboCt.csv', 'wb', buffering = 0))

    themeCtCSV.writerows(themeCt)

    return

if __name__ == '__main__':
    main()
