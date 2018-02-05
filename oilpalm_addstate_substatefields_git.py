#-------------------------------------------------------------------------------
# Name:        Add  Fields to Oil Palm
# Purpose:  add state and substate fields to oil palm dataset
# Author:      Ifeoma Collins, WRI, GIS Research Analyst II
#
# Created:     January 30, 2018
#Updated on: Feb 2, 2018

#-------------------------------------------------------------------------------

import arcpy, os, sys, string

import time
import random

then = time.time() #Time before the operations start

from arcpy import env
env.overwriteOutput = True

script_folder = r"C:\data\field_script" + "\\"

env.workspace = script_folder


#data


gfw_oil_palm = r"C:\data\field_script\gfw_oil_palm_server.shp"

merged_adm_clip = r"C:\data\field_script\adm\merge_adm2_idn_mys_cmr_lbr_cog_png_slb_clip.shp"

#merged adm data
arcpy.MakeFeatureLayer_management (merged_adm_clip, "merged_adm_lyr")

#create variables for each country

#countires (7)
#IDN
idn = "IDN"

#MYS
mys = "MYS"

#CMR
cmr = "CMR"

#LBR
lbr = "LBR"

#COG
cog = "COG"

#Papua New Guinea
png = "PNG"
png_oil = "Papua New Guinea"

#Solomon Islands
slb = "SLB"
slb_oil = 'Solomon Islands'

#adm fields
#state field
iso = "ISO"

name0 = "NAME_0"

state = "state"
name1 = "NAME_1"

#substate field
substate = "substate"
name2 = "NAME_2"


adm_fields = [state, substate]
country_oils = [idn, mys, cmr, lbr, cog, png_oil, slb_oil]
ISO_adms = [idn, mys, cmr, lbr, cog, png, slb]

featureclasses = arcpy.ListFeatureClasses()
print featureclasses
print "\n"
#do once
#add fields - state and substate
'''


for fc in featureclasses:#shapefile
    print fc
    for adm_field in adm_fields: #fields to add
        print adm_field
        #maybe make field length like 100, right now it's 75
        arcpy.AddField_management(fc,adm_field, "TEXT", "", "", 100)

    print "added state and substate fields for " + str(fc)
    print "\n"
'''
country_counter = 1
#go through oil palm layer
for fc in featureclasses:#shapefile

    #print "fc counter " + str(country_counter)

    fc_layer = fc[:-4] + "_lyr"
    arcpy.MakeFeatureLayer_management (fc, fc_layer)
    #print "feature class " + fc
    #print "feature layer " + fc_layer

    #country_counter = country_counter + 1
    for country_oil in country_oils: #go through countries
        print "\n"
        print "country # counter " + str(country_counter)
        country_counter = country_counter + 1
        print "New Country: " + country_oil
        where_clause = """ "country" = '""" + country_oil + """'""" #definition query for each country?

        polyFields = ["OID@", "state", "substate"]
        # Create update cursor for feature class
        #select all rows to make sure changed query
        #get count of rows to make sure country query worked
        arcpy.SelectLayerByAttribute_management (fc_layer, "NEW_SELECTION", where_clause)
        polygon_count = arcpy.GetCount_management(fc_layer)
        print "Number of total concessions is " + str(polygon_count) + " in " + country_oil + "\n"

        #account for png and slb
        if country_oil == png_oil:
            country_oil = png

        if country_oil == slb_oil:
            country_oil = slb

        where_clause_adm = """ "ISO" = '""" + country_oil + """'""" #definition query for adm

        #adm boundary search cursor
        adm_cursor =  arcpy.da.SearchCursor(merged_adm_clip, ['OID@', iso, name0, name1, name2], where_clause_adm)  #name fields
        for adm_row in adm_cursor:


                #get name from adm
                adm_fid = adm_row[0]
                adm_iso = adm_row[1]
                adm_country = adm_row[2]
                state_name =  adm_row[3]
                substate_name = adm_row[4]
                print "adm fid " + str(adm_fid)
                print "state name " + state_name
                print "substate name " + substate_name
                row_counter = 0

                if country_oil == png_oil:
                    country_oil = png

                if country_oil == slb_oil:
                    country_oil = slb

                print "\n"
                print "Adm ISO " + adm_iso + " equals country ISO " + country_oil + "\n"
                #select current row for adm cursor
                arcpy.SelectLayerByAttribute_management ("merged_adm_lyr", "NEW_SELECTION", "FID = {}".format(adm_row[0]))

                #number of selected in adm cursor
                admpolygon_count = arcpy.GetCount_management("merged_adm_lyr")
                print "Number of selected rows in the current adm polygon is (should be just 1) " + str(admpolygon_count) + "\n"

                #select oil palm concessions in current country that have their centroid in current adm boundary
                arcpy.SelectLayerByLocation_management (fc_layer, "HAVE_THEIR_CENTER_IN", "merged_adm_lyr")

                oil_polygon_result = arcpy.GetCount_management(fc_layer)
                oil_polygon_count =int(oil_polygon_result.getOutput(0)) #to get > 0 to work

                print "Number of selected concessions that are inside the current adm polygon is " + str(oil_polygon_count) + "\n"

                if country_oil == png:
                    country_oil = png_oil

                if country_oil == slb:
                    country_oil = slb_oil

                where_clause = """ "country" = '""" + country_oil + """'""" #definition query for each country?


                polycursor = arcpy.da.UpdateCursor(fc_layer, polyFields, where_clause) #poly cursor where clause is working

                #maybe should only update if greater than 0, a centroid intersection
                if oil_polygon_count > 0:

                    for polyrow in polycursor:
                        fid = polyrow[0]
                        print "fid " + str(fid)
                        print "\n"



                        #update values of right fields in oil palm
                        #name
                        polyrow[1] = state_name

                        #name1
                        polyrow[2] = substate_name
                        polycursor.updateRow(polyrow)

                        print "State Fields updated with " + state_name + " for " + country_oil + " adm id " + str(adm_fid) + " in fid " + str(fid)
                        print "SubState Fields updated with " + substate_name + " for " + country_oil + " adm id " + str(adm_fid)  + " in fid " + str(fid) + "\n"

                    del polyrow
                    del polycursor

        del adm_row
        del adm_cursor


now = time.time() #Time after it finished

print("It took: ", now-then, " seconds")
print "done" #44 seconds with no updates