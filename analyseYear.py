import os
import pandas as pd
import numpy as np

inFolder = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\Seasonal\AnalysedMonthly'
yearlyAvgDf = pd.DataFrame(columns=['year', 'average', 'StDev'])
for year in range(2000, 2020):
    yearFolder = str(year) + '_' + str(year+1)
    yearPath = os.path.join(inFolder, yearFolder)
    yearlySum = 0
    valueList = []
    for file in os.listdir(yearPath):
        if file.endswith('ValidOnly.csv'):
            df = pd.read_csv(os.path.join(yearPath, file))
            if pd.isnull(df['AverageSnow'].loc[df.index[2]]):
                value = 0
            else:
                value = df['AverageSnow'].loc[df.index[2]]
            yearlySum = yearlySum+value
            valueList.append(value)
    yearlyAvg = yearlySum/12
    std = np.std(valueList, ddof=1)
    #print('Yearly average for year '+ str(year) +' is '+str(yearlyAvg))
    yearlyAvgDf = yearlyAvgDf.append({'year': year, 'average': yearlyAvg, 'StDev': std}, ignore_index=True)
print(yearlyAvgDf)
yearlyAvgDf.to_csv((r"C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\All_Years_Averages_Summary.csv"), index=False)

