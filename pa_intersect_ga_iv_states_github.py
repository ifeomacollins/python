#Title: For each state in regions in Ghana and Ivory Coast, intersect the PA boundaries to the state boundary
#Author: Ifeoma Collins, GIS Research Analyst II
#Start Date: 8/21/17
#Finished date:
#Update Date:


import arcpy, os, sys, string

from arcpy import env
env.overwriteOutput = True

# Set folders for input and output
script_folder = r"C:\Users\ifeoma.collins\file" + "\\"
env.workspace = script_folder


#PA shapefiles for intersects
gh_pa_intersect = script_folder + "pa_gh_intersect.shp"
iv_pa_intersect = script_folder + "pa_iv_intersect.shp"



#folders
#output path
output =  r"C:\Users\ifeoma.collins\Documents\file\output" + "\\"


# Use the ListFeatureClasses function to return a list of shapefiles.
featureClasses = arcpy.ListFeatureClasses()


for fc in featureClasses:
    print fc
    print "\n"

    #find GH states shapefile
    if fc == "gh_c_region_states.shp":
        print "in GH c region state shapefile"
        print "\n"

        # Make a layer from the feature class
        arcpy.MakeFeatureLayer_management(fc, "gh_c_states_lyr")


        counter = 0
        #go through each row and select one state
        with arcpy.da.SearchCursor(fc, ['OID@', 'state']) as cursor:
            for row in cursor:
                #
                #print (row[1])
                state_name =  row[1]
                print state_name
                query = "state = '" + state_name + "' "
                print query
                arcpy.SelectLayerByAttribute_management("gh_c_states_lyr", "NEW_SELECTION", query)
                #print number of selected points
                sresult = arcpy.GetCount_management("gh_c_states_lyr")
                print "Number of selected rows in " + fc + " is " + str(sresult) + ".\n"

                #intersect with pa for GH with selected state name in file
                arcpy.Intersect_analysis([fc,gh_pa_intersect], output + "pa_gh_intersect_" + state_name + ".shp")

                counter = counter + 1
                print "\n"

            print "counter total was " + str(counter) + "\n"
            del row
            del cursor



#ivory coast
for fc1 in featureClasses:
    print fc1
    print "\n"

    #find IV c states shapefile
    if fc1 == "iv_c_region_states.shp":
        print "in IV c region state shapefile"
        print "\n"

        # Make a layer from the feature class
        arcpy.MakeFeatureLayer_management(fc1, "iv_c_states_lyr")


        counter = 0

        #go through each row and select one state
        with arcpy.da.SearchCursor(fc1, ['OID@', 'state']) as cursor:
            for row in cursor:
                #
                #print (row[1])
                state_name =  row[1]
                print state_name
                query = "state = '" + state_name + "' "
                print query
                arcpy.SelectLayerByAttribute_management("iv_c_states_lyr", "NEW_SELECTION", query)

                #print number of selected points
                sresult = arcpy.GetCount_management("iv_c_states_lyr")
                print "Number of selected rows in " + fc1 + " is " + str(sresult) + ".\n"

                #intersect with pa for IV with selected state name in file
                arcpy.Intersect_analysis([fc1,iv_pa_intersect], output + "pa_iv_intersect_" + state_name + ".shp")

                counter = counter + 1
                print "\n"

            print "counter total was " + str(counter) + "\n"
            del row
            del cursor

#del fc
del fc1
print "\n Done"

