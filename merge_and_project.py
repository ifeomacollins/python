#-------------------------------------------------------------------------------
# Name:        merge shapefiles into one and then project to wgs84
# Purpose:   merge shapefiles in different folders into one and then merged file to wgs
#
# Author:      Ifeoma Collins, WRI, GIS Research Analyst II
#
# Created:     May 10, 2018

#-------------------------------------------------------------------------------
import arcpy, os, sys, string
from glob import glob

import time

import random

#print "imports done"

then = time.time() #Time before the operations start

from arcpy import env
env.overwriteOutput = True

#print "env settings set"

#locations - have to do one for substate too
script_folder = r"C:\shapefiles" + "\\"
env.workspace = script_folder

print script_folder

cfile = "Area.shp"

merge_array = []

#list all folders in a directory
for root, dirs, files in os.walk(script_folder, topdown=False):
    for name in dirs:
        folder = os.path.join(root, name)
        cpath = folder + "\\" + cfile
        print cpath
        merge_array.append(cpath)


print "\n"

print merge_array

print "\n"

print "doing merge"

arcpy.Merge_management(merge_array, "merged_area.shp")

print "merge done, now changing projection"

# input data is in "SIRGAS 2000" projection
input_features = script_folder + "merged_area.shp"
output_feature_class = script_folder + "merged_area_projected.shp"
#out_coordinate_system = arcpy.SpatialReference('GCS_WGS_1984')
out_coordinate_system = sr = arcpy.SpatialReference(4326)
#out_coordinate_system = arcpy.SpatialReference('NAD 1983 StatePlane California V FIPS 0405 (US Feet)')


arcpy.Project_management(input_features, output_feature_class, out_coordinate_system)

print "projection done"

now = time.time() #Time after it finished

print("It took: ", now-then, " seconds")
print "done" #44 seconds with no updates
