# to do:
# - document


import os
import pandas as pd



def addDailyAverages(year, month, day, inputPath, df):
    fileName = 'MODIS_CloudFree_' + str(year) + '_'+ str(month) +'_' + str(day) + '.csv'
    dayFileDB = pd.read_csv(os.path.join(inputPath, str(year), str(month), fileName))
    sum = dayFileDB['gridcode'].sum()
    average = sum/347
    print(average)
    df.loc[len(df.index)] = [year, month, day, average]

allDailyAveragesDB = pd.DataFrame(columns=['year', 'month', 'day', 'SnowValue'])
inputPath = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\CloudFree'
for year in range(2000, 2021):
    if year == 2000:
        startMonth = 3
    else:
        startMonth = 1

    if year == 2020:
        endMonth = 7
    else:
        endMonth = 13
    for month in range(startMonth,endMonth):
        monthFolder = os.path.join(inputPath, str(year), str(month))
        for file in os.listdir(monthFolder):
            day = (file.split('_'))[-1].split('.')[0]
            try:
                addDailyAverages(year, month, day, inputPath, allDailyAveragesDB)
            except Exception as e:
                print(str(e)+ ' Month ' + str(year) + ' : ' + str(month) + ' : ' + str(day) +' failed¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬')
print(allDailyAveragesDB)
allDailyAveragesDB.to_csv(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\CloudFree\SuperSummarry.csv', index=False)
#dfValidOnly.to_csv(os.path.join(outFolder, str(month) + '_monthlySummaryValidOnly.csv'), index=False)