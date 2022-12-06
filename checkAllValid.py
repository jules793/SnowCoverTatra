'''
Two functions checkValid and checkAllPresent. To be run after the dataGap reduction script to ensure
all data points (each cell, for each day, in each year), are valid and present in the dataset.
Prints out error messages if a data gap is found.
Could be seperated into functions and called at the end of the data reduction script.
'''

import os
import pandas as pd
import datetime


#inFolder = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\outputCSVs'
newCloudFreeFolder = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\CloudFree'
oldCloudFreeFolder = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\OldCloudFree'

'''Check that all datapoints (each cell, in each day, in each year) in the dataset are valid.'''
def checkValid():
    for year in range(2000, 2021):
        print('Starts year '+ str(year))
        try:
            # EXCEPTION FOR YEAR 2000, first full month is march (3)
            if year == 2000:
                startMonth = 3
            else:
                startMonth = 1
            for month in range(startMonth, 13):
                monthPath = os.path.join(newCloudFreeFolder, str(year), str(month))
                for file in os.listdir(monthPath):
                    if file.endswith('.csv'):
                        day = int(file.split('_')[4].split('.')[0])
                        oldDB = pd.read_csv(os.path.join(monthPath, file))
                        oldDB.index = oldDB['pointid']
                        for index, row in oldDB.iterrows():
                            # Check for invalid data
                            if row['gridcode'] not in range(0,101):
                                #  ERROR case - invalid value was found, prints the location
                                print('INVALID GRIDCODE---------------------------------------------------------------------------------------------------------------------------------')
                                print(row['gridcode'], file)
        except Exception as e:
            print('ERROR OCCURED FOR YEAR:', str(year), e)


'''Check that all days from the beggining till the end of the study period are present in the dataset.'''
def checkAllPresent():
    date = datetime.date(2000, 3, 1)
    path = r'/outputCSVs/CloudFree'
    while date < datetime.date(2021,1,1):
        day = date.day
        month = date.month
        year = date.year
        file = 'MODIS_CloudFree_'+ str(year)+'_'+ str(month)+'_'+str(day)+'.csv'
        filePath = os.path.join(path, str(year), str(month), file)
        if not os.path.exists(filePath):
            # Error case - a day is missing
            print('FILE DOES NOT EXIST -----------------------------------------------------------------------------------------------------------------')
            print(file)
        date = date + datetime.timedelta(days=1)


checkValid()
checkAllPresent()


