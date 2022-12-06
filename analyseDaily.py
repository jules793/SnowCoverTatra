import os
import pandas as pd

# Takes a path to the month folder
def analyse(year, month, CSVsPath):
    monthPath = os.path.join(CSVsPath, str(year), str(month))
    # Creates a directry if it doesnt already exist
    if not os.path.isdir(os.path.join(CSVsPath, 'AnalysedDaily', str(year), str(month))):
        os.makedirs(os.path.join(CSVsPath, 'AnalysedDaily', str(year), str(month)))
    analysedDayPath = os.path.join(CSVsPath, 'AnalysedDaily', str(year), str(month))
    for file in os.listdir(monthPath):
        if file.endswith(".csv"):
            day = int(file.split('_')[4].split('.')[0])
            dfCSV = pd.read_csv(os.path.join(monthPath, file))
            newColumns = ['year', 'month','day', 'gridcode', 'meaning', 'total_area', 'count']
            dfNew = pd.DataFrame(columns=newColumns)
            for x in range(0, 101):
                counter = 0
                area = 0
                for index, row in dfCSV.iterrows():
                    if row['gridcode'] == x:
                        counter = counter+1
                        area = area + float(row['area'])
                dfNew.loc[len(dfNew.index)] = [year, month, day, x, 'Snow coverage percentage', area, counter]
            dfNew.to_csv(os.path.join(analysedDayPath, file), index=False)


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