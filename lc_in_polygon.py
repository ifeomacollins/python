#-------------------------------------------------------------------------------
# Name:
# Purpose:# Name: find the area in ha and % of total polygon that contains natural land cover category and update that info in corresponding fields
#
# Author:      Ifeoma Collins
#
# Created:     30/11/2017
# Copyright:   (c) icollins 2017

#-------------------------------------------------------------------------------

import arcpy, os, datetime, numpy

from datetime import datetime as DT #for sorting dates

from arcpy import env

# Set folders
shapefile_folder = r'U:\icollins\gfwc\scripts\policy\para'
env.workspace = shapefile_folder

env.overwriteOutput = True


#polygon
#para_poly = shapefile_folder + "\\" + "input_para_cattleranch.shp"
para_poly_lc = shapefile_folder + "\\" + "input_para_cattleranch_lcfields.shp" #for land cover wireframes

#Theme data ********************
#CREATE INTERSECTS MANUALLY
theme_folder = r'U:\icollins\gfwc\themes'

peat = theme_folder + "\\" + "peat.shp"

pa_int = shapefile_folder + "\\" + "data\\theme\\para_wdpa.shp"

ifl_int = shapefile_folder+ "\\" + "data\\theme\\para_ifl.shp"

pf = theme_folder + "\\" + "pf.shp"

lc_int = r'U:\icollins\gfwc\scripts\policy\para\data\theme\para_cattle_lc_proj.shp'

#create feature layer managment for following layers
para_ifl_lyr = "para_ifl_lyr"
arcpy.MakeFeatureLayer_management (ifl_int, para_ifl_lyr)

para_pa_lyr = "para_pa_lyr"
arcpy.MakeFeatureLayer_management (pa_int, para_pa_lyr)


#create new fields for natural land cover areas and %

#bare areas 200                   0
#broadleaved decidous 50, 60     1*
#broadleave evergeen/semi deci 40  2
#flooded broadleaved 160  3
#flooded vegetation 170, 180   4*
#grassland 140   5
#mixedbroadland 100   6
#mosaic of forest - 110, 120   7*
#needleleaved/deciduous - 70, 90  8*
#shrubland - 130  9
#sparesevegetation - 150   10

#need to account for cats with 2 numbers
grid_id = [200, [50, 60], 40, 160, [170, 180], 140, 100, [110, 120], [70, 90], 130, 150]

nat_lc_all = ["bare_ha", "bare_per", "brdeci_ha", "brdeci_per", "brev_ha", "brev_per", "flbl_ha", "flbl_per", "flvg_ha", "flvg_per", "grass_ha", "grass_per", "mix_ha", "mix_per", "mos_ha", "mos_per", "need_ha", "need_per", "shrub_ha", "shrub_per", "spar_ha", "spar_per"]
nat_lc = ["bare", "brdeci", "brev", "flbl",  "flvg",  "grass",  "mix", "mos",  "need",  "shrub",  "spar"]

nat_lc_stats = ["_ha", "_per"]

#need to assign each code to a category and right fields to update - use an array
nat_lc_combo = zip(nat_lc, grid_id)
'''
for lc in nat_lc:
    for stats in nat_lc_stats:
        lcfield = lc+stats
        print lcfield
        arcpy.AddField_management(para_poly_lc, lcfield, "FlOAT", "", "", "", "", "", "")

'''


#just do once***********

para_lc_lyr = "para_lc_lyr"
arcpy.MakeFeatureLayer_management (para_poly_lc, para_lc_lyr)

#natural land cover polygon for para
lc_int_lyr = "lc_int_lyr"
arcpy.MakeFeatureLayer_management (lc_int, lc_int_lyr)

para_fields = ["OID@", "area_ha", "bare_ha", "bare_per", "brdeci_ha", "brdeci_per", "brev_ha", "brev_per", "flbl_ha", "flbl_per", "flvg_ha", "flvg_per", "grass_ha", "grass_per", "mix_ha", "mix_per", "mos_ha", "mos_per", "need_ha", "need_per", "shrub_ha", "shrub_per", "spar_ha", "spar_per" ]
polycursor = arcpy.da.UpdateCursor(para_poly_lc, para_fields)
for polyrow in polycursor:
    #print "row counter " + str(row_counter)

    #fields
    print "\n"
    fid = polyrow[0]
    area_ha_para_poly = polyrow[1]
    #bare_ha = polyrow[2]   if i is 0 for bare, ha_field should be i+2;
    #bare_per = polyrow[3]                      per field should be i+3
    #brdeci_ha= polyrow[4]   if i is 1 for brdeci, ha_field should be i+3;
    #brdec_per = polyrow[5]                        per field should be i+4
    #brev_ha= polyrow[6]     if i is 2 for brev, ha_field should be i+4;
    #brev_per = polyrow[7]                       per field should be i+5

    print "fid " + str(fid)

    #fill out sections for land cover wire frames************************************

    #update cursor to go through each row in para polygon

    #select each row at a time
    #select current row
    arcpy.SelectLayerByAttribute_management (para_lc_lyr, "NEW_SELECTION", "FID = {}".format(polyrow[0]))
    #count number selected in polygon
    polygon_count = arcpy.GetCount_management(para_lc_lyr)
    print "Number of selected rows in the current Para LC polygon is " + str(polygon_count) + "\n"

    #go through each code type
    #query for each grid code one at a time
    #natural lc categories by grid number
    #ha counter

    #reset back to category 0 numbers for each row
    ha_counter = 2

    #percent counter
    pa_counter = 3


    for i in range (0,11): #range doesn't do the last number? for the the 11 categories in each row

        print "i: " + str(i)
        print "ha counter is " + str(ha_counter)
        print "per counter is " + str(pa_counter)

        #need to account for cats with more than one number
        if i == 1 or i== 4 or i== 7 or i== 8:
            grid_query = ' "gridcode" = ' + str(nat_lc_combo[i][1][0]) + ' OR "gridcode" =  ' + str(nat_lc_combo[i][1][1])
        else:
            grid_query = ' "gridcode" = ' + str(nat_lc_combo[i][1])

        print "grid num is " + str(nat_lc_combo[i][1]) + " and cat name is " + str(nat_lc_combo[i][0])
        print grid_query

        arcpy.SelectLayerByAttribute_management (lc_int_lyr, "NEW_SELECTION", grid_query)

        #count number selected in polys in natural lc
        all_lc_count = arcpy.GetCount_management(lc_int_lyr)
        print "Number of selected rows in land cover poly is " + str(all_lc_count)


        #if natural land cover type code not in lc polygon skip this land cover category...
        #if all_lc_count > 0:

        #select by location - the rows in the LUC current code - current selection that are WITHIN the current row in the polygon feature - CENTROID; WITHIN not getting all, intersect getting too many
        arcpy.SelectLayerByLocation_management (lc_int_lyr, "HAVE_THEIR_CENTER_IN", para_lc_lyr, "", "SUBSET_SELECTION")

        #get count
        lc_int_poly_count = arcpy.GetCount_management(lc_int_lyr)
        print "Number of selected rows in land cover poly in para poly row is " + str(lc_int_poly_count)

        #if count greater than 0, then do the following:
        #if lc_int_poly_count > 0:

        #find the sum of area_ha field
        area_ha = arcpy.da.TableToNumPyArray(lc_int_lyr, ('area_ha'))
        area_ha_sum = area_ha["area_ha"].sum()
        print "The total area in HA of the cat " +  str(nat_lc_combo[i][0]) + " in Para poly for FID row " + str(fid) + " is " + str(area_ha_sum)

        #get % in para cursor row with % number
        area_sum_percent = ((area_ha_sum/area_ha_para_poly)*100)

        print "The total area of the current Para poly is " + str(area_ha_para_poly)
        print "The total % of cat " + str(nat_lc_combo[i][0]) + " in Para poly for FID row " + str(fid) + " is " + str(area_sum_percent) + "\n"

        #need to get the right fields
        #update the right field HA in para cursor with this number
        polyrow[ha_counter]= area_ha_sum #using the variable doesn't update it for some reason....

        #update the right field % in para cursor row with % number
        polyrow[pa_counter]= area_sum_percent #using the variable doesn't update it for some reason....

        polycursor.updateRow(polyrow)

        #ha field counter
        #first: 2
        #second: 2 + 2  = 4
        #third: 4 + 2  = 6

        ha_counter = ha_counter + 2

        #percent counter
        #first: 3
        #second: 3 + 2  = 5
        #third: 5 + 2 = 7
        pa_counter = pa_counter + 2

        #11 land use categories
        #already on indvidual fid row
        #for row 19


del polyrow
del polycursor

print "done"