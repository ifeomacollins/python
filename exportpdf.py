# Export maps to pdf in year 1 construction schools folder
#Project : Stosur School 1, ArcGIS 10.1
#Created by: Melissa Oguamanam, Baltimore City of Planning
#Start Date: September 12, 2013
#Finished: 9/12/2013
#Updated on: 3/27/2014
#Purpose: The script will interate through each MXD in a folder
#export them as a pdf in a new folder called ----

import arcpy, os
#from arcpy.mapping import *

from arcpy import env

#define workspace/ path to main project folder of year 1
env.overwriteOutput = True
env.workspace = 'M:\\Projdata\\Schools\\Neighborhood Planning Process\\Facilities\\march27\\'

datapath = 'M:\\Projdata\\Schools\\Neighborhood Planning Process\\Facilities\\march27\\'
pdfpath = datapath + 'script\\'   #output for pdfs


#listmaps = arcpy.ListFiles("*.mxd")

#loop through workspace, find all mxds and export as pdf using the same name as mxd for
for mxdfile in arcpy.ListFiles("*.mxd"):
    print datapath + mxdfile
    mxd = arcpy.mapping.MapDocument(datapath + mxdfile)
    #print mxd
    mxdshort = mxdfile.strip('.mxd')
    arcpy.mapping.ExportToPDF(mxd, pdfpath + mxdshort + '.pdf')
    del mxd


