#-------------------------------------------------------------------------------
# Name:        Count fires in concessions annually
# Purpose:   to count the number of MODIS fires annually in Indonesia for individual companies, sumatara island, kalimantan island, total outside wood fiber, total inside wood fiber
#
# Author:      Ifeoma Collins, WRI, GIS Research Analyst II
#
# Created:     Nov 17 - 2017

#-------------------------------------------------------------------------------


import arcpy, os, sys, string

from arcpy import env
env.overwriteOutput = True

# Set folders for input and output
fire_script_folder = r"C:\Documents\data\asia\Indonesia\forest_concessions\fire_count_script" + "\\"
years_folder = r"C:\Documents\data\asia\Indonesia\forest_concessions\fire_count_script\add_yr" + "\\"
years_folder_test = r"C:\Documents\data\asia\Indonesia\forest_concessions\ire_count_script\add_yr\test" + "\\"
env.workspace = years_folder


#create variables for each dataset

#fire points
fires = fire_script_folder + "fires\\fires_nov_2011_2017_ind_sum_kali.shp"

'''
#comp all companies
comp = fire_script_folder + "ind_wood_fiber_comp.shp"

#comp dissolved
comp_dissolved = fire_script_folder + "ind_wood_fiber_comp_dissolve.shp"

#Sumatra
sumatra = fire_script_folder + "ind_sumatra.shp"

#Kalimantan
kali = fire_script_folder + "ind_kalimatan.shp"

#All wood fiber concessions
wood_fiber = fire_script_folder + "ind_wood_fiber.shp"

#Islands without wood fiber concessions
no_woodfiber = fire_script_folder + "ind_sum_ka_wf_erase.shp"
'''

#Loop through shapefiles in workspace
featureclasses = arcpy.ListFeatureClasses() #get a list of shapefiles
print featureclasses

#year fields array
years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]

#list fc
'''
for fc in featureclasses:#shapefile
    print fc
    for year in years: #years
        fieldName = "yr_" + str(year)
        arcpy.AddField_management(fc,fieldName, "LONG")

    print "added all year fields for " + str(fc)
    print "\n"

'''
#add fields for each year to polygons 2001-2017; long type
#just do once then turn off

#fires point data
arcpy.MakeFeatureLayer_management (fires, "fireslyr")

#go through each dataset
for fc in featureclasses:#shapefile
    fc_counter = 0
    print "fc counter " + str(fc_counter)

    fc_layer = fc[:-4] + "_lyr"
    arcpy.MakeFeatureLayer_management (fc, fc_layer)
    print "feature class " + fc
    print "feature layer " + fc_layer

    fc_counter = fc_counter + 1

    for year in years: #years
        yr_counter = 2001
        print "yr counter " + str(yr_counter)
        print "current year " + str(year)

        #polygon data
        fieldName = "yr_" + str(year)
        polyFields = ["OID@", fieldName]
        # Create update cursor for feature class
        polycursor = arcpy.da.UpdateCursor(fc, polyFields)



        for polyrow in polycursor:
            row_counter = 0
            print "row counter " + str(row_counter)

            #name fields
            fid = polyrow[0]
            polyYrfield = polyrow[1]

            print fid

            #select current row
            arcpy.SelectLayerByAttribute_management (fc_layer, "NEW_SELECTION", "FID = {}".format(polyrow[0]))
            #count number selected in polygon
            polygon_count = arcpy.GetCount_management(fc_layer)
            print "Number of selected rows in the current polygon is " + str(polygon_count) + "\n"

            #fires points
            #for current year, select all points in that year in fires data
            #arcpy.SelectLayerByAttribute_management ("fireslyr", "NEW_SELECTION", " [Year] = '" + str(year) + "' ")
            arcpy.SelectLayerByAttribute_management ("fireslyr", "NEW_SELECTION", """ "Year" = '""" + str(year) + """'""")

            #count number selected in fire points
            all_fires_count_yr = arcpy.GetCount_management("fireslyr")
            print "Number of selected rows in fires is " + str(all_fires_count_yr) + " for year " + str(year) + "\n"

            #select by location number of selected fire points for that year that intersect with each feature in current dataset
            arcpy.SelectLayerByLocation_management ("fireslyr", "INTERSECT", fc_layer, "", "SUBSET_SELECTION")

            #count number of points selected within polygon intersection
            poly_fires_in_yr = arcpy.GetCount_management("fireslyr")
            print "Number of selected rows in fires is " + str(poly_fires_in_yr) + " for year " + str(year) + " that instersect the feature row " + str(fid) + "\n"

            poly_fires_result = int(arcpy.GetCount_management("fireslyr").getOutput(0)) ## must add the int and getoutput or won't read as integer
            print "poly_fires_result is " + str(poly_fires_result)
            #add number of points sum count to the corresponding year yr_year field for the right year/update cursor
            polyrow[1] = poly_fires_result
            polycursor.updateRow(polyrow)

            print str(fid) + " updated"
            row_counter = row_counter + 1
            yr_counter = yr_counter + 1

        del polyrow
        del polycursor


    print "added all year fields for " + str(fc)
    print "\n"

del fc

del featureclasses


print "done"