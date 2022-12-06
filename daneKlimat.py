import os
from zipfile import ZipFile
import pandas as pd
import datetime
import matplotlib.pyplot as plt


# Unzips downloaded folders
def unzipFiles():
    url = r'C:\My Web Sites\daneSynoptyczne\danepubliczne.imgw.pl\data\dane_pomiarowo_obserwacyjne\dane_meteorologiczne\dobowe\klimat'
    for folder in os.listdir(url):
        isFolder = os.path.isdir(os.path.join(url, folder))
        if isFolder and folder != '2000':
            for file in os.listdir(os.path.join(url, folder)):
                if file.endswith('.zip'):
                    print('Unzipping: ', file)
                    with ZipFile(os.path.join(url, folder, file), 'r') as zObject:
                        zObject.extractall(path=os.path.join(url, folder))
                else:
                    print('Not a zip file: ', file)


# Deletes zip files. Can be chnged to deleted chosen type of files
def deleteFiles():
    url = r'C:\My Web Sites\daneSynoptyczne\danepubliczne.imgw.pl\data\dane_pomiarowo_obserwacyjne\dane_meteorologiczne\dobowe\klimat'
    for folder in os.listdir(url):
        isFolder = os.path.isdir(os.path.join(url, folder))
        if isFolder and folder!='2000':
            for file in os.listdir(os.path.join(url, folder)):
                if file.endswith('.zip'):
                    print('Deleted: ', file)
                    os.remove(os.path.join(url, folder, file))
                else:
                    print('Untouched: ', file)

# Adds headers to the raw download files.
def addHead():
    url = r'C:\My Web Sites\daneSynoptyczne\danepubliczne.imgw.pl\data\dane_pomiarowo_obserwacyjne\dane_meteorologiczne\dobowe\klimat'
    headers = ['StationCode', 'StationName','Year','Month', 'Day', 'AverageTemp', 'Precipitation', 'PrecipitationType', 'SnowLayerHeight']
    for folder in os.listdir(url):
        isFolder = os.path.isdir(os.path.join(url, folder))
        if isFolder:
            for file in os.listdir(os.path.join(url, folder)):
                if file.startswith('k_d'):
                    df = pd.read_csv(os.path.join(url, folder, file), usecols=[0,1,2,3,4,9,13,15,16], index_col=False, names=headers).fillna(0)
                    df.to_csv(os.path.join(url, folder, 'new_'+file), sep=',',index=False)


# Helper function to check what files contain data on the stations in the Tatra region.
# Outputs a file that is checked manually.
def checkStations():
    url = r'C:\My Web Sites\daneSynoptyczne\danepubliczne.imgw.pl\data\dane_pomiarowo_obserwacyjne\dane_meteorologiczne\dobowe\klimat'
    outputDF = pd.DataFrame(columns=['StationCode', 'StationName', 'FileFound'])
    for folder in os.listdir(url):
        isFolder = os.path.isdir(os.path.join(url, folder))
        if isFolder:
            for file in os.listdir(os.path.join(url, folder)):
                if file.startswith('new_k_d'):
                    print(file)
                    df = pd.read_csv(os.path.join(url, folder, file))
                    halaGas = False
                    halaOrnak = False
                    polChoch = False
                    dol5 = False
                    for index, row in df.iterrows():
                        if row['StationCode'] == 249200540:
                            halaGas = True
                        if row['StationCode'] == 249190680:
                            halaOrnak = True
                        if row['StationCode'] == 249190670:
                            polChoch = True
                        if row['StationCode'] == 249200550:
                            dol5 = True
                    if halaGas:
                        outputDF.loc[len(outputDF.index)] = [249200540, 'HALA GASIENICOWA', file]
                    if halaOrnak:
                        outputDF.loc[len(outputDF.index)] = [249190680, 'HALA ORNAK', file]
                    if polChoch:
                        outputDF.loc[len(outputDF.index)] = [249190670, 'POLANA CHOCHOLOWSK', file]
                    if dol5:
                        outputDF.loc[len(outputDF.index)] = [249200550, 'DOLINA PIECIU STAWOW', file]
    outputDF.to_csv(os.path.join(url, 'Summarry.csv'))


# Extracts stations located in the Tatra region from the general monthly files for klimat data.
def extractStations():
    url = r'C:\My Web Sites\daneSynoptyczne\danepubliczne.imgw.pl\data\dane_pomiarowo_obserwacyjne\dane_meteorologiczne\dobowe\klimat'
    headers = ['StationCode', 'StationName', 'Year', 'Month', 'Day', 'AverageTemp', 'Precipitation',
               'PrecipitationType', 'SnowLayerHeight']
    for folder in os.listdir(url):
        isFolder = os.path.isdir(os.path.join(url, folder))
        if isFolder:
            for file in os.listdir(os.path.join(url, folder)):
                if file.startswith('new_k_d'):
                    newDF = pd.DataFrame(columns=headers)
                    df = pd.read_csv(os.path.join(url, folder, file))
                    for index, row in df.iterrows():
                        code = row['StationCode']
                        tatraStation = bool((code==249200540) or
                                            (code==249190680) or
                                            (code==249190670) or
                                            (code==249200550))
                        if tatraStation:
                            my_series = df.iloc[index].squeeze()
                            newDF = newDF.append(my_series, ignore_index=True)
                    newDF.to_csv(os.path.join(url,folder, 'selected_'+file), index=False)


# Split a file with all selected stations included in one csv into seperate csv files for each station. Creates monthly.
def splitStations():
    url = r'C:\My Web Sites\daneSynoptyczne\danepubliczne.imgw.pl\data\dane_pomiarowo_obserwacyjne\dane_meteorologiczne\dobowe\klimat'
    headers = ['StationCode', 'StationName', 'Year', 'Month', 'Day', 'AverageTemp', 'Precipitation',
               'PrecipitationType', 'SnowLayerHeight']
    for folder in os.listdir(url):
        isFolder = os.path.isdir(os.path.join(url, folder))
        if isFolder:
            for file in os.listdir(os.path.join(url, folder)):
                if file.startswith('selected_new_k_d'):
                    hGasDF = pd.DataFrame(columns=headers)
                    hOrnakDF = pd.DataFrame(columns=headers)
                    pChochDF = pd.DataFrame(columns=headers)
                    d5DF = pd.DataFrame(columns=headers)
                    df = pd.read_csv(os.path.join(url, folder, file))
                    for index, row in df.iterrows():
                        if row['StationCode'] == 249200540:
                            my_series = df.iloc[index].squeeze()
                            hGasDF = hGasDF.append(my_series, ignore_index=True)
                        if row['StationCode'] == 249190680:
                            my_series = df.iloc[index].squeeze()
                            hOrnakDF = hOrnakDF.append(my_series, ignore_index=True)
                        if row['StationCode'] == 249190670:
                            my_series = df.iloc[index].squeeze()
                            pChochDF = pChochDF.append(my_series, ignore_index=True)
                        if row['StationCode'] == 249200550:
                            my_series = df.iloc[index].squeeze()
                            d5DF = d5DF.append(my_series, ignore_index=True)
                    hGasDF.to_csv(os.path.join(url,folder, 'HalaGas_'+file), index=False)
                    hOrnakDF.to_csv(os.path.join(url, folder, 'HalaOrnak_' + file), index=False)
                    pChochDF.to_csv(os.path.join(url, folder, 'PolanaChoch_' + file), index=False)
                    d5DF.to_csv(os.path.join(url, folder, 'Dolina5st_' + file), index=False)


# Function to merge monthly files for all klimat stations into yearly files. Only applicable to klimat dataset
def mergeMonths(url, headers):
    for folder in os.listdir(url):
        isFolder = os.path.isdir(os.path.join(url, folder))
        if isFolder:
            hGasDF = pd.DataFrame(columns=headers)
            hOrnakDF = pd.DataFrame(columns=headers)
            pChochDF = pd.DataFrame(columns=headers)
            d5DF = pd.DataFrame(columns=headers)
            for file in os.listdir(os.path.join(url, folder)):
                if file.startswith('Dolina5st_selected'):
                    df = pd.read_csv(os.path.join(url, folder, file))
                    d5DF = d5DF.append(df)
                if file.startswith('HalaGas_selected'):
                    df = pd.read_csv(os.path.join(url, folder, file))
                    hGasDF = hGasDF.append(df)
                if file.startswith('HalaOrnak_selected'):
                    df = pd.read_csv(os.path.join(url, folder, file))
                    hOrnakDF = hOrnakDF.append(df)
                if file.startswith('PolanaChoch_selected'):
                    df = pd.read_csv(os.path.join(url, folder, file))
                    pChochDF = pChochDF.append(df)
            d5DF.to_csv(os.path.join(url, 'DolinaPieciuStawow', 'Dolina5Stawow_'+str(folder)+'.csv'))
            hGasDF.to_csv(os.path.join(url, 'HalaGasienicowa', 'HalaGas_' + str(folder)+'.csv'))
            hOrnakDF.to_csv(os.path.join(url, 'HalaOrnak', 'HalaOrnak_' + str(folder)+'.csv'))
            pChochDF.to_csv(os.path.join(url, 'PolanaChocholowska', 'PolanaChoch_' + str(folder)+'.csv'))


# Function to merge yearly csv files into  a single file
def mergeYears(station, url, headers):
    stationPath = os.path.join(url, station)
    yearDF = pd.DataFrame(columns=headers)
    for file in os.listdir(stationPath):
        monthDF = pd.read_csv(os.path.join(stationPath, file))
        yearDF = yearDF.append(monthDF)
    yearDF.to_csv(os.path.join(url, stationPath, 'allYears'+station+'.csv'))


# Function to split a csv with all years into July-June files. Seasonal years.
def splitSeasons(station, headers,url):
    yearFilePath = os.path.join(url, station, 'allYears'+station+'.csv')
    yearDF = pd.read_csv(yearFilePath)
    for year in range(2000, 2021):
        print('Staring year ', year)
        seasonsYear = pd.DataFrame(columns=headers)
        for index, row in yearDF.iterrows():
            date = datetime.datetime(row['Year'], row['Month'], row['Day'])
            lastJune = datetime.datetime(year, 6, 30)
            nextJuly = datetime.datetime(year+1, 7, 1)
            if date <  nextJuly and date>lastJune:
                my_series = yearDF.iloc[index].squeeze()
                seasonsYear = seasonsYear.append(my_series, ignore_index=True)
        seasonsYear.to_csv(os.path.join(url, station, 'JUL'+str(year)+'_JUN'+str(year+1)+'_'+station+'.csv'))


# Function to plot snow height throughout one year for one station.
def plot(station, column, url, minY, maxY):
    for file in os.listdir(os.path.join(url, station)):
        if file.startswith('JUL'):
            year = file.split('L')[1][0:4]
            filePath = os.path.join(url, station, file)
            df = pd.read_csv(filePath)
            snowList = df[column].tolist()
            yearList = df['Year'].tolist()
            monthList = df['Month'].tolist()
            dayList = df['Day'].tolist()
            dateList = []
            for x in range(len(yearList)):
                dateList.append(datetime.datetime(yearList[x], monthList[x], dayList[x]))
            # PLOTTING
            fig = plt.figure(figsize=(8, 6))
            plt.plot(dateList, snowList)
            plt.grid( which='major', axis='both')
            plt.ylim(top=maxY)
            plt.ylim(bottom=minY)
            plt.xlabel("Time")
            plt.ylabel(column)
            font1 = {'size': 20}
            plt.title(str(station)+ ' July '+str(year)+ ' - June '+str(int(year)+1), fontdict=font1)
            fig.savefig(os.path.join(url, station, 'plots',column+file+'_plot.jpg'), bbox_inches='tight', dpi=150)
            plt.show()
            #plt.close(fig)


# Helper function used in plotMultiple.
def createList(n):
    lst = []
    for i in range(n+1):
        lst.append(i)
    return(lst)


# Function to plot all years 2000-2020 on the same graph. Should be called for each station
def plotMultiple(station, column, url):
    # {2000:(snowList, dateList), ...}
    dataSeries = {}
    for year in range(2000, 2021):
        fileName = 'JUL'+str(year)+'_JUN'+str(year+1)+'_'+station+'.csv'
        filePath = os.path.join(url, station, fileName)
        # Creating the list with snow layer height data
        df = pd.read_csv(filePath)
        snowList = df[column].tolist()
        # Making a list with 365 numbers for all 365 days in a year
        dateList =createList(365)
        # Creating the dictionary entry for given year
        dataSeries[year] = (snowList, dateList)
    # Setting up the plot
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(1, 1, 1)
    # Color ramp to be used for incremental years
    colorList =['#FA0000','#EE0C00','#E21800','#D62400','#CA3000','#BE3C00','#B24800','#A65500','#9A6100','#8E6D00',
                '#827900','#778500','#6B9100','#5F9D00','#53AA00','#47B600','#3BC200','#2FCE00','#23DA00','#17E600',
                '#0BF200','#00FF00']
    # Plotting a line for each year. Uses the colors from the list above. Weird calling of the datasets due to odd years
    for year in range(2000, 2021):
        plt.plot(createList(len(dataSeries[year][0])-1), dataSeries[year][0],
                 label=str(year), color=list(reversed(colorList))[year-2000])
    # Formatting the plot
    plt.grid( which='major', axis='both')
    plt.xlabel("Time")
    plt.ylabel(column)
    font1 = {'size': 20}
    plt.title((str(station) + ' 2000 - 2020'), fontdict=font1)
    # Inverting the legend so 2000 is at the bottom
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='center left')
    # Saving the plot jpg
    fig.savefig(os.path.join(url, station, 'plots',column+'Summary_plot.jpg'), bbox_inches='tight', dpi=150)
    plt.show()


# Helper function to check what should be the maximum y range for plotting individual years.
def plotYear(station, url, column):
    filePath = os.path.join(url, station, 'allYears' + station + '.csv')
    df = pd.read_csv(filePath)
    snowList = df[column].tolist()
    yearList = df['Year'].tolist()
    monthList = df['Month'].tolist()
    dayList = df['Day'].tolist()
    dateList = []
    for x in range(len(yearList)):
        dateList.append(datetime.datetime(yearList[x], monthList[x], dayList[x]))
    plt.plot(dateList, snowList)
    plt.grid(which='major', axis='both')
    plt.xlabel("Time")
    plt.ylabel("Snow Layer Height [cm]")
    plt.title(station)
    plt.show()

def plotSnowTempYear(station, url):
    for file in os.listdir(os.path.join(url, station)):
        if file.startswith('JUL'):
            year = file.split('L')[1][0:4]
            filePath = os.path.join(url, station, file)
            df = pd.read_csv(filePath)
            snowList = df['SnowLayerHeight'].tolist()
            tempList = df['AverageTemp'].tolist()
            yearList = df['Year'].tolist()
            monthList = df['Month'].tolist()
            dayList = df['Day'].tolist()
            dateList = []
            for x in range(len(yearList)):
                dateList.append(datetime.datetime(yearList[x], monthList[x], dayList[x]))
            # PLOTTING
            fig = plt.figure(figsize=(8, 6))
            plt.plot(dateList, snowList)
            plt.plot(dateList, tempList)
            plt.grid( which='major', axis='both')
            #plt.ylim(top=maxY)
            #plt.ylim(bottom=minY)
            plt.xlabel("Time")
            #plt.ylabel(column)
            font1 = {'size': 20}
            plt.title(str(station)+ ' July '+str(year)+ ' - June '+str(int(year)+1), fontdict=font1)
            fig.savefig(os.path.join(url, station, 'plots','tempSnow_'+file+'_plot.jpg'), bbox_inches='tight', dpi=150)
            plt.show()
            #plt.close(fig)




urlSynop = r'C:\My Web Sites\daneSynoptyczne\danepubliczne.imgw.pl\data\dane_pomiarowo_obserwacyjne\dane_meteorologiczne\dobowe\synop'
urlKlimat = r'C:\My Web Sites\daneSynoptyczne\danepubliczne.imgw.pl\data\dane_pomiarowo_obserwacyjne\dane_meteorologiczne\dobowe\klimat'
headersKlimat = ['StationCode', 'StationName', 'Year', 'Month', 'Day', 'AverageTemp', 'Precipitation',
                 'PrecipitationType', 'SnowLayerHeight']
headersSynop = ['StationCode', 'StationName', 'Year', 'Month', 'Day', 'AverageTemp', 'Precipitation',
                'PrecipitationType', 'SnowLayerHeight', 'SnowWaterEquivalent']
#unzipFiles()
#deleteFiles()
#addHead()
#checkStations()
#extractStations()
#splitStations()
#mergeMonths()
# mergeYears('DolinaPieciuStawow')
#splitSeasons('PolanaChocholowska')

#plotYear('DolinaPieciuStawow')
#plot('DolinaPieciuStawow', 330)
#plotYear('HalaOrnak')
#plot('HalaOrnak', 220)
#plotYear('HalaGasienicowa')
#plot('HalaGasienicowa', 280)
#plotYear('PolanaChocholowska')
#plot('PolanaChocholowska', 200)
#
# plotMultiple('DolinaPieciuStawow', urlKlimat)
# plotMultiple('HalaOrnak', urlKlimat)
# plotMultiple('HalaGasienicowa', urlKlimat)
# plotMultiple('PolanaChocholowska',urlKlimat)
# plotMultiple('Zakopane', urlSynop)
# plotMultiple('Kasprowy', urlSynop)

#PLOTTING TEMPERATURE
#plotYear('Kasprowy', urlSynop, 'AverageTemp')
#plot('Kasprowy', 'AverageTemp', urlSynop, -30, 20)
#plotMultiple('Kasprowy','AverageTemp', urlSynop)

#plotYear('Zakopane', urlSynop, 'AverageTemp')
#plot('Zakopane', 'AverageTemp', urlSynop, -25, 30)
#plotMultiple('Zakopane', 'AverageTemp',urlSynop)

#plotYear('DolinaPieciuStawow', urlKlimat, 'AverageTemp')
#plot('DolinaPieciuStawow', 'AverageTemp', urlKlimat, -25, 25)
#plotMultiple('DolinaPieciuStawow', 'AverageTemp',urlKlimat)

#plotYear('HalaOrnak', urlKlimat, 'AverageTemp')
#plot('HalaOrnak', 'AverageTemp', urlKlimat, -25, 25)
#plotMultiple('HalaOrnak', 'AverageTemp',urlKlimat)

#plotYear('HalaGasienicowa', urlKlimat, 'AverageTemp')
#plot('HalaGasienicowa', 'AverageTemp', urlKlimat, -25, 25)
#plotMultiple('HalaGasienicowa', 'AverageTemp',urlKlimat)

#plotYear('PolanaChocholowska', urlKlimat, 'AverageTemp')
#plot('PolanaChocholowska', 'AverageTemp', urlKlimat, -25, 25)
#plotMultiple('PolanaChocholowska', 'AverageTemp',urlKlimat)

#plotSnowTempYear('Zakopane', urlSynop)