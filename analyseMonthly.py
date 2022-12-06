# to do:
# - document


import os
import pandas as pd

def analyse(year, month, CSVsPath):
    inFolder = os.path.join(CSVsPath, 'AnalysedDaily', str(year), str(month))
    newColumns = ['year', 'month', 'gridcode', 'meaning', 'total_area', 'Total_Count']
    dfValidOnly = pd.DataFrame(columns=newColumns)
    for x in range(0, 101):
        counter = 0
        area = 0
        for file in os.listdir(inFolder):
            if file.endswith(".csv"):
                dfCSV = pd.read_csv(os.path.join(inFolder, file))
                for index, row in dfCSV.iterrows():
                    if row['gridcode'] == x:
                        counter = counter + float(row['count'])
                        area = area + float(row['total_area'])
        dfValidOnly.loc[len(dfValidOnly.index)] = [year, month, x, 'Snow coverage percentage', area, counter]

    dfValidOnly['Weighted'] = dfValidOnly['gridcode']*dfValidOnly['Total_Count']
    WeightedSum = dfValidOnly['Weighted'].sum()
    CountSum = dfValidOnly['Total_Count'].sum()
    if CountSum != 0:
        AverageSnow = WeightedSum/CountSum
    else:
        AverageSnow = 0
    dfValidOnly['AverageSnow'] = AverageSnow

    if not os.path.isdir(os.path.join(CSVsPath, 'AnalysedMonthly', str(year))):
        os.makedirs(os.path.join(CSVsPath, 'AnalysedMonthly', str(year)))

    outFolder = os.path.join(CSVsPath, 'AnalysedMonthly', str(year))
    dfValidOnly.to_csv(os.path.join(outFolder, str(month) + '_monthlySummaryValidOnly.csv'), index=False)


for year in range(2000, 2020):
    if year == 2000:
        startYear = 3
    else:
        startYear = 1
    for month in range(startYear,13):
        try:
            analyse(year, month, r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\CloudFree')
            print("Finished " + str(year) + ' : ' + str(month))
        except:
            print('Month ' + str(year) + ' : ' + str(month) + ' failed¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬')