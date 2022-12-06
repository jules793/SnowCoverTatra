''' Creates a big file with all monthly averages throughout the study period.'''

import os
import pandas as pd

inputPath = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\Seasonal\AnalysedMonthly'

newDB = pd.DataFrame(columns=['year', 'month', 'averageSnowCover'])

for element in os.listdir(inputPath):
    if os.path.isdir(os.path.join(inputPath, element)):
        yearFolderPath = os.path.join(inputPath, element)
        for monthFile in os.listdir(yearFolderPath):
            monthDB = pd.read_csv(os.path.join(yearFolderPath, monthFile))
            year = monthDB['year'].loc[monthDB.index[0]]
            month = monthDB['month'].loc[monthDB.index[0]]
            averageSnow = monthDB['AverageSnow'].loc[monthDB.index[0]]
            newDB.loc[len(newDB.index)] = [year, month, averageSnow]
print(newDB)
newDB.to_csv(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\Seasonal\AnalysedMonthly\All_MonthlyAverages.csv')




