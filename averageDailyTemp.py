
import os
import pandas as pd


def incompleteStation(station):
    pathString = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\METEO\klimat\AllYearsAllStations\allYears' + station + '.csv'
    stationDB = pd.read_csv(pathString)
    for index, row in newDB.iterrows():
        for stationIndex, stationRow in stationDB.iterrows():
            if stationRow['Year']==row['year'] and stationRow['Month']==row['month'] and stationRow['Day']==row['day']:
                print('found the value for: ', row['year'], row['month'], row['day'] )
                newDB.at[index, station] = stationRow['Precipitation']

inputPath = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\METEO\klimat\AllYearsAllStations'
newDB = pd.DataFrame(columns=['year', 'month', 'day', 'date','HalaOrnak', 'Zakopane', 'DolinaPieciuStawow', 'HalaGaienicowa', 'Kasprowy', 'PolanaChocholowska', 'AverageTemp'])
datesFile = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\dates.csv'
datesDB = pd.read_csv(datesFile)
ZakopaneDB = pd.read_csv(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\METEO\klimat\AllYearsAllStations\allYearsZakopane.csv')
KasprowyDB = pd.read_csv(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\METEO\klimat\AllYearsAllStations\allYearsKasprowy.csv')

#for file in os.listdir(inputPath):

newDB['year'] = datesDB['year']
newDB['month'] = datesDB['month']
newDB['day'] = datesDB['day']
newDB['date'] = datesDB['date']

#newDB['Zakopane'] = ZakopaneDB['Precipitation']
#newDB.to_csv(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\DailyPrecAverages.csv', index=False)
#newDB['Kasprowy'] = KasprowyDB['Precipitation']
#newDB.to_csv(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\DailyPrecAverages.csv', index=False)

# try:
#     incompleteStation('HalaOrnak')
#     print('finished Hala Ornak')
# except:
#     print('error')
# newDB.to_csv(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\DailyPrecAverages.csv', index=False)

try:
    incompleteStation('HalaGasienicowa')
    print('finished Hala Gas')
except:
    print('error')
newDB.to_csv(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\DailyPrecAveragesHalGas.csv', index=False)

try:
    incompleteStation('DolinaPieciuStawow')
    print('finished dol piec')
except:
    print('error')
newDB.to_csv(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\DailyPrecAveragesDolPiec.csv', index=False)

# try:
#     incompleteStation('PolanaChocholowska')
# except Exception:
#     print(Exception)


print (newDB.to_string())
newDB.to_csv(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\DailyPrecAveragesGasPiec.csv', index=False)