from openpyxl import load_workbook

import csv, getSysArgs, re


def main():
    print 'Usage Note:\nIf there are formulas on the sheet you would like to convert to CSV, save a new xlsx file of the sheet with the formulas changed to their values.'

    ## CSV file of Tweets and data
    [fName, sheetname] = getSysArgs.usage(['xlsx2csv.py', '<XLSX_file_path>',
                                '<sheetname_to_convert>'])[1:]

    ## Open Excel file
    dataXL = load_workbook(fName)

    ## Worksheet to convert
    ws = dataXL[sheetname].rows

    ## Stores values of spreadsheet for CSV version of file
    sheetVals = []

    for row in ws:
        ## List of row values
        rowVals = []

        for cell in row:
            ## Cell value
            cVal = cell.value

            ## Data type
            cType = type(cVal)

            if cType is str or cType is unicode:
                cVal = cVal.encode('utf-8')

            rowVals.append(cVal)

        sheetVals.append(rowVals)

    ## CSV version of file
    dataCSV = csv.writer(open(fName.replace('.xlsx', '.csv'), 'wb',
                              buffering = 0))

    dataCSV.writerows(sheetVals)
    return

if __name__ == '__main__':
    main()
