'''Creates yearly files with an average snow cover for each cell'''
import os
import pandas as pd

inputPath = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\Seasonal\CellAverages'
outputPath =r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\Seasonal\CellAverages\Yearly'
monthTranslationDict = {1:7, 2:8, 3:9, 4:10, 5:11, 6:12, 7:1, 8:2, 9:3, 10:4, 11:5, 12:6}
for yearFolder in os.listdir(inputPath):
    if yearFolder.startswith('20'):
        year = yearFolder.split('_')[0]
        print(year)
        yearFolderPath = os.path.join(inputPath, yearFolder)
        yearDB = pd.DataFrame(columns=['year', 'pointid', 'averageSnowValue'])
        # for one month
        for cell in range(0, 347):
            # for one cell, one month average
            yearSum = 0
            monthCount = 0
            for file in os.listdir(yearFolderPath):
                monthDB = pd.read_csv(os.path.join(yearFolderPath, file))
                value = monthDB['averageSnowValue'].loc[monthDB.index[cell]]
                yearSum = yearSum + value
                monthCount = monthCount + 1
            average = yearSum/monthCount
            print('Average for cell ', str(cell), ' for year ', year, ' : ', average)
            pointid = int(monthDB['pointid'].loc[monthDB.index[cell]])
            # get year value from the file as they are organised seasonally so 2 different years in each one 'year' folder
            yearDB.loc[len(yearDB.index)] = [year, pointid, average]
        newFileName = 'Year_Cell_Averages_'+ str(int(year)) +'.csv'
        yearDB.to_csv(os.path.join(outputPath, newFileName), index=False)

