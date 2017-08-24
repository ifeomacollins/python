#Convert thousands of gpx points to polygon
#author: Ifeoma Collins, GIS Research Analyst II, World Resources Insitute
#Date: 8/23/17
#Finished: 8/24/17
#Updated on:


# Import system modules
import arcpy, os, sys, logging, shutil
from arcpy import env
env.overwriteOutput = True

# -*- coding: utf-8 -*-
import unidecode #to remove special characters from file names


logging.basicConfig(filename=r"U:\icollins\c\m\iv\not_in_iv.txt", level=logging.INFO)

# Set folders
data_folders = r'U:\icollins\c\m\iv'
env.workspace = data_folders

workspaces = arcpy.ListWorkspaces("*")


#individual folders
gpx_folder = r'U:\icollins\c\m\iv\GPX' + "\\"
shp_point = "shp\point" + "\\"
shp_line = "shp\line" + "\\"
shp_polygon = "shp\polygon" + "\\"
shp_dissolve = "shp\polygon\dissolve" + "\\"
bad_data = gpx_folder + "bad_data" + "\\"


iv = r'U:\icollins\c\m\iv\CIV_adm0.shp'

env.workspace = gpx_folder


for gpx_file in arcpy.ListFiles("*.gpx"):
    print gpx_file

    #correct file names before process
    #have to fill spaces in names with underscores...
    new_gpx_file_name_white_space = gpx_file.replace(" ", "_")

    #replace ' with _
    new_gpx_file_name_apos = new_gpx_file_name_white_space.replace("'", "_")

    #replace ( with _
    new_gpx_file_name_left_para = new_gpx_file_name_apos.replace("(", "_")

    #replace ) with _
    new_gpx_file_name_right_para = new_gpx_file_name_left_para.replace(")", "_")

    #replace . with _
    new_gpx_file_name_right_period = new_gpx_file_name_right_para[:-4].replace(".", "_")

    #replace - with _
    new_gpx_file_name_dash =  new_gpx_file_name_right_period.replace("-", "_")



    #remove characters with diacritics #don't need apparently #maybe the utf code will do
    #convert to unicode string
    #new_gpx_file_name_unicode = unicode(new_gpx_file_name_dash, 'utf-8')

    #noaccent_gpx_file_name = unidecode.unidecode(new_gpx_file_name_unicode)
    #print noaccent_gpx_file_name

    #gpx_file = noaccent_gpx_file_name
    gpx_file_output = new_gpx_file_name_dash

    print gpx_file_output



    #GPX to features
    #Converts the point information inside a GPX file into features.
    Input_GPX_File = gpx_folder + gpx_file
    Output_Feature_class_points = gpx_folder + shp_point + gpx_file_output[:-4] + ".shp"
    print Input_GPX_File
    print Output_Feature_class_points

    #handling errors for features that can't be converted to points, lines, or polygons
    try:

        arcpy.GPXtoFeatures_conversion (Input_GPX_File, Output_Feature_class_points)
        print "gpx conversion to points shp done"

        #points to line
        #Creates line features from points. close line to convert to polygon
        Output_Feature_class_lines = gpx_folder + shp_line + gpx_file_output[:-4] + ".shp"
        print Output_Feature_class_lines
        arcpy.PointsToLine_management(Output_Feature_class_points, Output_Feature_class_lines, "", "", 'CLOSE')
        print "points converted to lines"

        #feature to polygon
        #Creates a feature class containing polygons generated from areas enclosed by input line or polygon features.
        Output_Feature_class_polygons = gpx_folder + shp_polygon + gpx_file_output[:-4] + ".shp"
        print Output_Feature_class_polygons
        arcpy.FeatureToPolygon_management(Output_Feature_class_lines, Output_Feature_class_polygons)
        print "lines converted to polygon"



        #may want to dissolve into one
        Output_Feature_class_polygons_dissolved = gpx_folder + shp_dissolve + gpx_file_output[:-4] + ".shp"
        print Output_Feature_class_polygons_dissolved
        arcpy.Dissolve_management(Output_Feature_class_polygons, Output_Feature_class_polygons_dissolved, "", "", "MULTI_PART", "")
        print "polygon feautures dissolved into one"


        #check to see if polygon fully within IV
        #make feature layer
        dissolved_lyr = "dissolved_" + gpx_file_output[:-4]
        print dissolved_lyr
        arcpy.MakeFeatureLayer_management(Output_Feature_class_polygons_dissolved, dissolved_lyr)

        #select by location if polygon if fully within IV - only select those that don't intersect
        arcpy.SelectLayerByLocation_management (dissolved_lyr, "WITHIN_CLEMENTINI", iv, "", "", "INVERT" )

        #get count
        getcount = int(arcpy.GetCount_management(dissolved_lyr)[0])

        counter_IV = 0
        #if not, write shapefile name into a log file
        if getcount == 1:
            print dissolved_lyr + " is not fully within IV."
            logging.info(Output_Feature_class_polygons_dissolved + " is not within country.")
            counter_IV = counter_IV + 1
        else:
            print "Layer is within country!"

    except:
        print gpx_file + " contains bad data that can't be converted to a line, point, or polygon"
        #move to bad data folder
        shutil.move(Input_GPX_File, bad_data + gpx_file)


del gpx_file, Output_Feature_class_polygons_dissolved
print counter_IV
print "done"
