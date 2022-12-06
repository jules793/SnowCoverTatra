
# Make pretty version of the daily csv in pandas, save as csv in new folder, with an extra column for corrected values.
# Build directory in script.

# Loop through days in a month (files in the new month folder). Check if pixel (pointid) is cloud or polar night.
# If YES, check day after, day before, 2 days after, 2 days before, 3 days after, 3 days before in the original column.
# DEAL WITH days in different months/years.
# If a valid gridcode is found, add it to the new column and move to the next day. If not, copy the invalid code.
# If the original value was valid - copy it to the new column

import os
import pandas as pd
import datetime
import shutil

#inFolder = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\outputCSVs'
newCloudFreeFolder = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\CloudFree'
oldCloudFreeFolder = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\OldCloudFree'

def getNewGridCode(action, num, pointid, day, month, year, inFolder):
    current = datetime.date(year, month, day)
    if action =='add':
        newDate = current + datetime.timedelta(days = num)
    elif action == 'substract':
        newDate = current - datetime.timedelta(days=num)
    # Exception case for the end of the entire dataset
    if newDate>datetime.date(2020,12,31):
        newGridCode = '255'
    else:
        newDay = newDate.day
        newMonth = newDate.month
        newYear = newDate.year
        newFile = 'MODIS_CloudFree_' + str(newYear) + '_' + str(newMonth) + '_' + str(newDay) + '.csv'
        #print('Day before file: ' + oneBeforeFile)
        newPath = os.path.join(inFolder, str(newYear), str(newMonth), newFile)
        newDB = pd.read_csv(newPath)
        newDB.index = newDB['pointid']
        newGridCode = newDB.at[pointid, 'gridcode']
        #print('GridCode day before: '+str(newGridCode))
    return newGridCode

fileChanged = True
runcount = 0
while fileChanged:
    runcount = runcount+1
    fileChanged = False
    if os.path.exists(newCloudFreeFolder):
        print('new cloud free exists')
        os.rename(os.path.join(newCloudFreeFolder), os.path.join(oldCloudFreeFolder))
        print('Directory should be renamed')
    else:
        # Exception case for the first ever iteration of the cloud-free function
        oldCloudFreeFolder = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs'
    os.makedirs(newCloudFreeFolder)

    for year in range(2000, 2021):
        print('Starts year '+ str(year))

        try:
            if not os.path.exists(os.path.join(newCloudFreeFolder, str(year))):
                os.makedirs(os.path.join(newCloudFreeFolder, str(year)))

            # EXCEPTION FOR YEAR 2000, first full month is march (3)
            if year == 2000:
                startMonth = 3
            else:
                startMonth = 1

            #for month in range(6, 8):
            for month in range(startMonth, 13):
                if not os.path.exists(os.path.join(newCloudFreeFolder, str(year), str(month))):
                    os.makedirs(os.path.join(newCloudFreeFolder, str(year), str(month)))
                    print('should make a new month folder')
                # Delete all files already in the month folder - for rerunning the script
                dir = os.path.join(newCloudFreeFolder, str(year), str(month))
                for f in os.listdir(dir):
                    os.remove(os.path.join(dir, f))

                monthPath = os.path.join(oldCloudFreeFolder, str(year), str(month))
                newDB = pd.DataFrame(columns=['year', 'month', 'day', 'gridcode', 'area'])

                # Setting up the new pointid column whichis used as index
                for file in os.listdir(monthPath):
                    if file.endswith('.csv'):
                        oldDB = pd.read_csv(os.path.join(monthPath, file))
                        oldDB.index = oldDB['pointid']
                        for index, row in oldDB.iterrows():
                            newDB.at[index, 'pointid'] = row['pointid']
                newDB.index = newDB['pointid']

                newDB['year'] = year
                newDB['month'] = month

                for file in os.listdir(monthPath):
                    if file.endswith('.csv'):
                        print('Original file: '+ file+ '¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬')
                        day = int(file.split('_')[4].split('.')[0])
                        #print(day)
                        newDB['day'] = day
                        #print(newDB.to_string())

                        oldDB = pd.read_csv(os.path.join(monthPath, file))
                        oldDB.index = oldDB['pointid']

                        for index, row in oldDB.iterrows():
                            # Check for cloud or polar night
                            if row['gridcode'] not in range(0, 101):
                                #print('correcting')
                                fileChanged = True
                                # Do the hard bit
                                # Check day before
                                # calculate one before day
                                #print('Index: '+ str(index))
                                oneBefore = getNewGridCode('substract', 1, index, day, month, year, oldCloudFreeFolder)
                                if oneBefore in range(0, 101):
                                    newValue = oneBefore
                                else:
                                    oneAfter = getNewGridCode('add', 1, index, day, month, year, oldCloudFreeFolder)
                                    if oneAfter in range(0, 101):
                                        newValue = oneAfter
                                    else:
                                        twoBefore = getNewGridCode('substract', 2, index, day, month, year, oldCloudFreeFolder)
                                        if twoBefore in range(0, 101):
                                            newValue = twoBefore
                                        else:
                                            twoAfter = getNewGridCode('add', 2, index, day, month, year, oldCloudFreeFolder)
                                            if twoAfter in range(0, 101):
                                                newValue = twoAfter
                                            else:
                                                threeBefore = getNewGridCode('substract', 3, index, day, month, year, oldCloudFreeFolder)
                                                if threeBefore in range(0, 101):
                                                    newValue = threeBefore
                                                else:
                                                    threeAfter = getNewGridCode('add', 3, index, day, month, year, oldCloudFreeFolder)
                                                    if threeAfter in range(0, 101):
                                                        newValue = threeAfter
                                                    else:
                                                        newValue = row['gridcode']
                            else:
                                newValue = row['gridcode']

                            newDB.at[index, 'gridcode']= newValue
                            newDB.at[index, 'area'] = row['area']
                        # print('OLD DATABASE for '+ file)
                        # print(oldDB)
                        # print('NEW DATABASE:')
                        # print(newDB)
                    outputFileName = 'MODIS_CloudFree_'+ str(year)+'_'+ str(month)+ '_'+str(day)+ '.csv'
                    newDB.to_csv(os.path.join(newCloudFreeFolder, str(year), str(month), outputFileName), sep=',', index=False)
        except Exception as e: print('ERROR OCCURED FOR YEAR:', str(year), e)


    if fileChanged:
        print('A FILE HAS BEEN CHANGED. NEEDS TO BE RERUN')
    else:
        print('NO FILE HAS BEEN CHANGED. CLOUD FREE PROCESS COMPLETE. ALL DATA SHOULD NOW BE VALID')
    shutil.rmtree(oldCloudFreeFolder)

print(runcount )

