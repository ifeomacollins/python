# -*- coding: utf-8 -*-
"""
Created on Friday, October 27, 2023
Analyze deforestation in Brazil state from 1992 - 2020.
Identify which land cover types replaced forests in Rondônia, Brazil. 
Based on ESRI Climate Change Class
@author: Ifeoma Collins

"""

import os, time, glob
import numpy as np
import datetime as dt


import arcpy
from arcpy import env
from arcpy.sa import *

arcpy.CheckOutExtension('Spatial') #need license for certain tools


then = time.time() #Time before the operations start


#reclassify to simple numbers/classes


#raster calculator subtraction 

#symbolize change

print ("Modules are imported")
print ("\n")

print("Starting script now to calculate deforestation rate")
print ("\n")
print ("\n")


arcpy.env.workspace = r"\\Documents\projects\global_landcover\RondoniaDeforestation" + "\\"


#Before start, manually export rasters to make own copy to work on in desktop; save as tif
#save in a new folder

'''
#list rasters in folder
raster_list = arcpy.ListRasters("*")


#print (raster_list)
#or do the following to print rasters in array

for raster in raster_list:
    print ("\n")
    print (raster)
    TheRows=arcpy.SearchCursor(raster)

    for TheRow in TheRows:
       TheClassName=TheRow.getValue("ClassName")
       print(TheClassName)

    #reclassify to simplify land use
    # Set local variables

   
    print ("\n")
    inRaster = raster
    print ("reclassifying this raster now: " + inRaster)
    reclassField = "ClassName"

    
    #use remapvalue
    #must put text with spaces in single quotes
    remap = RemapValue([["'Urban Areas'", 1],
                        ["'Rainfed Cropland'", 10], ["'Herbaceous Cropland'", 10],["'Mostly Cropland in a Mosaic with Natural Vegetation'", 10],["'Mostly Natural Vegetation in a Mosaic with Cropland'", 10],
                        ["'Closed to Open Canopy Broadleaved Evergreen Tree Cover'", 100],["'Closed to Open Canopy Broadleaved Deciduous Tree Cover'", 100],["'Closed Canopy Broadleaved Deciduous Tree Cover'", 100],["'Closed to Open Canopy Needleleaved Deciduous Tree Cover'", 100],
                        ["'Mostly Trees and Shrubs in a Mosaic with Herbaceous Cover'", 100],["'Mostly Herbaceous Cover in a Mosaic with Trees and Shrubs'", 100],
                        ["'Shrubland'", 1000],["'Grassland'", 1000],["'Flooded Shrub or Herbaceous Cover'", 1000],["'Saline Water Flooded Tree Cover'", 1000], ["'Fresh or Brackish Water Flooded Tree Cover'", 1000],
                        ["'Bodies of Water'", 100000],["'Bare Areas'", 10000]])

    # Execute Reclassify
    outReclassify = Reclassify(inRaster, reclassField, remap, "NODATA")

    # Save the output with reclassify folder #output must end in file type (ex. .tif)
    outReclassify.save(r"\\Documents\projects\global_landcover\RondoniaDeforestation\reclassify" + "\\" + raster)
    print ("reclassifying is complete for this raster:" + raster)
    print ("\n")
    '''
   


#now use reclassified rasters created above
#list rasters in reclassified folder

arcpy.env.workspace = r"\\Documents\projects\global_landcover\RondoniaDeforestation\reclassify" + "\\"

raster_list2 = arcpy.ListRasters("*")

#get field values

for reclass_raster in raster_list2:
    print ("\n")
    print (reclass_raster)
    TheRows=arcpy.SearchCursor(reclass_raster)

    for TheRow in TheRows:
       TheClassName=TheRow.getValue("ClassName")
       print(TheClassName)



#subtract rasters / map algebra
# Set local variables
inRaster1 = Raster("Ron_LC_2020_copy.tif")
inRaster2 = Raster("Ron_LC_1992_copy.tif")
print ("\n")
print ("Found rasters to subtract")

# Execute Minus
outMinus = inRaster1 - inRaster2
print ("\n")
print ("Doing raster subtract")

# Save the output 
outMinus.save(r"\\Documents\projects\global_landcover\RondoniaDeforestation\reclassify\subtract\Ron_LC_2020_minus_1992.tif")
print ("\n")
print ("Saved raster extract")


#add field
#add category type for 3 main
#add area field
#caculate area of changes

print ("\n")

now = time.time() #Time after it finished

print("This script took: ", now-then, "seconds to finish.")
print ("done")
