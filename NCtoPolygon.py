'''Script for the initial raw data processing. Includes the 'rawDataProcessing function.
Starts by asigning variables and setting up the ArcGIS workspace with Tatra Park files.
Section at the end calls the function.
Should be refactored to have the function in  seperate file.'''

import arcpy
import os


if not arcpy.Exists(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\MODIS_GIS\workspaceGDB.gdb'):
    arcpy.management.CreateFileGDB(r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\MODIS_GIS\\', 'workspaceGDB')
arcpy.env.workspace = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\MODIS_GIS\workspaceGDB.gdb'
for cl in arcpy.ListFeatureClasses():
    arcpy.Delete_management(cl)
for r in arcpy.ListRasters():
    arcpy.Delete_management(r)

#DATAfolder = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\'
workspaceGDB = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\MODIS_GIS\workspaceGDB.gdb'
natPark = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\TatraNationalPark\TatraNationalPark.shp'
tatraRegionPolygon = r"C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\TatraRegion\TatraRegionPolygon.shp"
tatraRegionVertices = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\TatraRegion\TatraRegionVertices.shp'
CEDApath = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\CEDA'
SHPOutputFolder = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputSHP\\'
CSVOutputFolder = r'C:\Users\Julia\Documents\UofG\Dissertation\DATA\MODIS_data\outputCSVs\\'

arcpy.FeatureClassToGeodatabase_conversion(tatraRegionPolygon, workspaceGDB)
arcpy.FeatureClassToGeodatabase_conversion(natPark, workspaceGDB)
arcpy.FeatureClassToGeodatabase_conversion(tatraRegionVertices, workspaceGDB)


def rawDataProcessing(year, month, path):
    monthcounter = month
    yearCounter = year
    CEDApath = path
    #month loop
    for file in os.listdir(os.path.join(CEDApath, str(yearCounter), str(monthcounter))):
        fileStr = str(file)[6] + str(file)[7]
        daycounter = int(fileStr)
        print(fileStr)
        print(file)
        ncFile = os.path.join(CEDApath, str(yearCounter), str(monthcounter), file)
        print(ncFile)
        name = 'MODIS' + '_' + str(yearCounter) + '_' + str(monthcounter) + '_' + str(daycounter)

        arcpy.md.MakeNetCDFRasterLayer(str(ncFile), 'scfg', 'lon', 'lat', name)
        print('Made a raster from nc ' + name)

        rectExtract = arcpy.sa.ExtractByRectangle(name, tatraRegionPolygon, 'INSIDE')
        rectExtract.save(os.path.join(workspaceGDB, name + 'rectExtract'))
        print('Extracted by rectangle')

        pointName = name + '_Points'
        arcpy.conversion.RasterToPoint(rectExtract, pointName)
        print('raster to point done')
        arcpy.analysis.Buffer(pointName, pointName+'_Buffer', '0.005 DecimalDegrees')
        print('point to buffer')
        arcpy.management.MinimumBoundingGeometry(pointName+'_Buffer', name+'_MBG', 'ENVELOPE')
        print('polygon around point')
        arcpy.analysis.Clip(name+'_MBG', natPark, name+'_PolygonGrid')
        print('clipped to the park')
        arcpy.management.AddGeometryAttributes(name+'_PolygonGrid', 'CENTROID', 'METERS', 'SQUARE_METERS')
        # Save output shp and csv
        outputSHP = os.path.join(SHPOutputFolder, str(yearCounter), str(monthcounter))
        arcpy.FeatureClassToFeatureClass_conversion(name+'_PolygonGrid', outputSHP, name+'_TatraPolygon.shp')
        outputCSV = os.path.join(CSVOutputFolder, str(yearCounter), str(monthcounter))
        arcpy.conversion.TableToTable(name + '_PolygonGrid', outputCSV, name+'FinalTable.csv')

        for cl in arcpy.ListFeatureClasses():
            arcpy.Delete_management(cl)
        for r in arcpy.ListRasters():
            arcpy.Delete_management(r)


for x in range(10,11):
    try:
        rawDataProcessing(2000, x, CEDApath)
        print("2000 finished month" + str(x))
    except: print('month '+ str(x)+ 'failed ¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬')