#Project: Finding average lot size acres for counties
#Created by: Melissa Oguamanam, IT Programmer Analyst 2, MD dept of Planning
#Start Date: June 18, 2015
#Finished: June 22, 2015
#Updated on:
#Purpose: find average acres and number of improved parcel points btwn 2002/2012 by zoning by protective genzone by county
#average_acres.mxd
#part2 after diss_county_gen_zoning.shp is fixed manually....

# Import ArcPy site-package to use Arcgis and os modules to use operating system
import arcpy, os, sys, string, numpy
from arcpy import env
env.overwriteOutput = True

#set environment settings to where mxd is saved
env.workspace = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\zoningdistrict_avg_acres'

#folders
datapath = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\zoningdistrict_avg_acres' + "\\"
mxdpath = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\zoningdistrict_avg_acres' + "\\"
output = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\zoningdistrict_avg_acres\output' + "\\"
diss_output = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\zoningdistrict_avg_acres\data\dissolve' + "\\"
diss_union = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\zoningdistrict_avg_acres\data\union' + "\\"

#for parcel point locations
parcel_path_pre = r'J:\GIS_WORK\PDS_WORK_Area\Mdpv2012' + "\\"
parcel_path_post = r'\ATDATA\DATABASE' + "\\"


for mxdfile in arcpy.ListFiles("*.mxd"):   #linked to where workspace is set # keep 1 mxd in folder #only going through here once
   print mxdpath + mxdfile
   mxd = arcpy.mapping.MapDocument(datapath + mxdfile)
   df = arcpy.mapping.ListDataFrames(mxd)
   lyr = arcpy.mapping.ListLayers(mxd)
   
   #access different layers in mxd
   clyr = arcpy.mapping.ListLayers(mxd, "Counties") 
   glyr = arcpy.mapping.ListLayers(mxd, "gener*")
   countgenzonlyr = arcpy.mapping.ListLayers(mxd, "diss_county_gen_zoning")

   #print countgenzonlyr

   #loop through every layer in dataframe #get access to correct layers
   
   for dataFrame in df:          #loop dataframes

       #go to parcel points group layer
               for layer in lyr:
                   if layer.isGroupLayer and layer.longName=="Parcel Points":  #only walk through shapefiles in grouplayer
                       #sublayers. parcel2012 shapefiles
                       for sublayer in layer: #region name
                           #for subsublayer in sublayer:  #actual parcel point shapefiles for each county
                           print sublayer
                           #print sublayer.name
                           #make value of jurscode; minus last 4 characters and capitlize it
                           parcel_jurscode=sublayer.name[:-4].upper()
                           print "Parcel jurscode is now " + parcel_jurscode

                           parcel_feat_class = parcel_path_pre + sublayer.name + parcel_path_post + sublayer.name + '.shp'
                           print parcel_feat_class
                           arcpy.MakeFeatureLayer_management(parcel_feat_class, sublayer)  #optional? Not optional!
                           parcel_query_result = arcpy.GetCount_management(sublayer)
                           print "Total rows for parcel " + str(parcel_query_result) + "\n"

                           #need to do select query for 2002-2012 improved parcels
                           sublayer.definitionQuery= ' "YEARBLT" >= \'2002\' AND "YEARBLT" <= \'2012\' AND ( "LU" = \'A\' OR "LU"= \'R\' OR "LU"=\'TH\' OR "LU" = \'U\') AND "ACRES" <= 20 AND "NFMIMPVL" >= 10000'
                           parcel_query_result = arcpy.GetCount_management(sublayer)
                           print "Number of rows that meet parcel query criteria is " + str(parcel_query_result) + "\n"

                           

                           #county/gen/zoning shapefile
                           for countgenzon in countgenzonlyr:
                               print countgenzon

                               ### 1. select the dissolved county gen zone file
                               cgz_feat_class = diss_output + countgenzon.name + '.shp'
                               print cgz_feat_class
                               arcpy.MakeFeatureLayer_management(cgz_feat_class, countgenzon.name)  #optional? Not optional!
                               #keep track of selections to make sure is working
                               countgen_query_result = arcpy.GetCount_management(cgz_feat_class)
                               print "Number of rows in count gen zone originally is " + str(countgen_query_result) + "\n"
                               #select rows that match the county of the current parcel point shapefile
                               #arcpy.SelectLayerByAttribute_management(countgenzon.name, "NEW_SELECTION", """ "JURSCODE" = '""" + parcel_jurscode + """'""")
                               countgenzon.definitionQuery= """ "JURSCODE" = '""" + parcel_jurscode + """'"""
                               countgen_query_result = arcpy.GetCount_management(countgenzon)
                               print "Number of rows in count gen zone that match current parcel point county is " + str(countgen_query_result) + "\n"

                               #create a cursor to go through every row in county/gen/zoning file
                               #search first - get collection of rows from feature class
                               inTable = cgz_feat_class  
                               urows = arcpy.da.UpdateCursor(inTable,["OID@", "JURSCODE", "FID", "Parcels", "ACRES", "AvgLotSize"] ,where_clause=""" "JURSCODE" = '""" + parcel_jurscode + """'""")  #have to use da.searchcursor to get oid

                               #srow=srows.next()
                               counter = 0
                               
                               #create a variable to hold value of attributes in specific row
                               for urow in urows:
                                  #here
                                  #
                                  #parcels
                                  

                                  #print srow[0]
                                  jurscode_cty = urow[1]     #have to use srow for da.searchsursor
                                  fid= urow[0]              #have to use srow for da.searchsursor 
                                  #jurscode_cty = srow.getValue("JURSCODE")
                                  #fid= srow.getValue("FID")
                                  counter = counter + 1
                                  #print jurscode_cty

                                  arcpy.SelectLayerByAttribute_management(countgenzon.name, "NEW_SELECTION", "FID= {}".format(urow[0]))    #have to use srow for da.searchsursor
                                  arcpy.SelectLayerByLocation_management(sublayer, 'HAVE_THEIR_CENTER_IN', countgenzon.name)
                                  #number of parcel points that intersect the current row..
                                  parcel_query_result = int(arcpy.GetCount_management(sublayer).getOutput(0))  ## must add the int and getoutput or won't read as integer

                                  ######CODE REPEATS HERE
                                  print "FID: " + str(fid) +  " county: " + str(jurscode_cty) +" Number of rows that meet parcel query criteria and intersect the county protective gen zoning layer is " + str(parcel_query_result) + "\n"

                                  
                                  inFeatures1 = sublayer
                                  arr = arcpy.da.TableToNumPyArray(inFeatures1, ('ACRES'))
                                  acres_sum = arr["ACRES"].sum()
                                  print "The total sum of acres in " +  str(jurscode_cty) + " parcel points for FID row " + str(fid) + " is " + str(acres_sum) + "\n"

                                  #print parcel_query_result

                                  ucounter = 0

                                  if parcel_query_result > 0:
                                     #
                                     print str(parcel_query_result) + " parcels. Will be updating the fields."
                                     

                                     #urow.Parcels = parcel_query_result
                                     #urow.ACRES = acres_sum
                                     #urow.AvgLotSize = (acres_sum/parcel_query_result)
                                     urow[3] = parcel_query_result
                                     urow[4] = acres_sum
                                     urow[5] = (acres_sum/parcel_query_result)
                                     print parcel_query_result
                                     print acres_sum
                                     print (acres_sum/parcel_query_result)

                                     urows.updateRow(urow)
                                     print str(fid) + " row values updated with parcels, acres sum, and avg lot size" + "\n"

                                       

                                  else:
                                     print "0 parcels in select by location. No updating fields. Moving to next row."

                                  ucounter = ucounter + 1
                                  print "number of times gone through if parcels > 0 loop is " + str(ucounter)
                            



                               print str(counter) + "\n \n"   #should be 214 features in the diss county gen zone shapefile
                               del urow
                               del urows


                               #find parcel points that have jurscode equal jurscode of row in countygenzone cursor. make that query for the parcel points

                               #then find parcel points that intersect the feature row

                               #count the number of parcel points that meet this criteria. add number to parcels field in row

                               #sum up the acres field from the selected features and add the acres field

                               #find average: acres/parcels. put in avglotssize field

      
            
                   
                   
del mxdfile, mxd
print '\n Done'
