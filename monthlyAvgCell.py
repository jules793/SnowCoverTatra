''' Calculates monthly averages of seperate cells. Produces monthly files with cell averages'''
import os
import pandas as pd

inputPath = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\Seasonal'
outputPath =r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\Seasonal\CellAverages'
for yearFolder in os.listdir(inputPath):
    if yearFolder.startswith('20'):
        year = yearFolder.split('_')[0]
        yearFolderPath = os.path.join(inputPath, yearFolder)
        # for one month
        for monthFolder in os.listdir(yearFolderPath):
            month = monthFolder.split('_')[0]
            monthFolderPath = os.path.join(yearFolderPath, monthFolder)
            monthDB = pd.DataFrame(columns=['year', 'month', 'pointid', 'averageSnowValue'])
            for cell in range(0, 347):
                # for one cell, one month average
                monthSum = 0
                dayCount = 0
                for file in os.listdir(monthFolderPath):
                    dayDB = pd.read_csv(os.path.join(monthFolderPath, file))
                    value = dayDB['gridcode'].loc[dayDB.index[cell]]
                    monthSum = monthSum + value
                    dayCount = dayCount + 1
                average = monthSum/dayCount
                #print('Average for cell ', str(cell) , ' for month ', month, ' : ', average)
                pointid = int(dayDB['pointid'].loc[dayDB.index[cell]])
                # get year value from the file as they are organised seasonally so 2 different years in each one 'year' folder
                year = dayDB['year'].loc[dayDB.index[cell]]
                # get month value from the file too
                month = dayDB['month'].loc[dayDB.index[cell]]
                monthDB.loc[len(monthDB.index)] = [year, month, pointid, average]
            newFileName = 'Month_Cell_Averages_'+ str(year)+'_'+ str(month) + '.csv'
            monthDB.to_csv(os.path.join(outputPath, yearFolder, newFileName), index=False)

