''' Creates 12 monthly files with cell averages over the entire study period'''

import os
import pandas as pd

''' A function that takes a month and creates a file with average cell values in that month over 20 years'''
def createMonthlyAverage(month):
    for year in range(2000, 2020):
        basePath = r"C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\Seasonal\CellAverages"
        filePath = r"C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\Seasonal\CellAverages\2000_2001\Month_Cell_Averages_2000_7.csv"
        fileName = 'Month_Cell_Averages_' +  + '.csv'
        filePath = os.path.join(basePath, yearFolder, )

inputPath = r"C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\Seasonal\CellAverages"


for month in range(1, 13):
    newDB = pd.DataFrame(columns=['month', 'pointid', 'average'])
    for cell in range(0, 347):
        cellSum = 0
        for year in range(2000, 2020):
            yearFolder = str(year) + '_' + str(year+1)
            if month <= 6:
                yearCorrected = year +1
            else:
                yearCorrected = year
            fileName = 'Month_Cell_Averages_' + str(yearCorrected) +'_'+ str(month) + '.csv'
            filePath = os.path.join(inputPath, yearFolder, fileName)
            monthDB = pd.read_csv(filePath)
            value = monthDB['averageSnowValue'].loc[monthDB.index[cell]]
            cellSum = cellSum +value
        cellAvg = cellSum/20
        pointid = int(monthDB['pointid'].loc[monthDB.index[cell]])
        newDB.loc[len(newDB.index)] = [month, pointid, cellAvg]
    print(newDB)
    exportFile = 'Month_Average_Cells_'+str(month)+'.csv'
    exportPath = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\Seasonal\CellAverages\monthly'
    newDB.to_csv(os.path.join(exportPath, exportFile), index=False)