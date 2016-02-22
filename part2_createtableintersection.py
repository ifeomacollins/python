#Project:
#Created by: Melissa Oguamanam Baltimore City of Planning
#Start Date: October 4, 2013
#Finished:
#Updated on:
#Purpose: for each shapefile in flood extent, create new field in attribute table
#put 1-5 (number) in a each field corresponding to extent if exists


# Import ArcPy site-package to use Arcgis and os modules to use operating system
import arcpy, os

# define workspaces/data path variables
from arcpy import env
env.overwriteOutput = True
env.workspace = r'T:\03Comprehensive_Planning\Environmental\Sustainability\Disaster Preparedness and Planning Project (DP3)\DP3 Charts and Maps\moguam\HAZUS\ken\scripts\ken101013'

datapath = r'T:\03Comprehensive_Planning\Environmental\Sustainability\Disaster Preparedness and Planning Project (DP3)\DP3 Charts and Maps\moguam\HAZUS\ken'
pdfpath = datapath + '\\pdf\\'   #output for pdfs
mappath = datapath + '\\scripts\\ken101013\\'
shppath = datapath + '\\scripts\\ken101013\\new\\'



print 'List of map document:'

##############

#Go through list of Shapefiles/layers* in .mxd*/folder?
#loop through workspace, find all mxds 
for mxdfile in arcpy.ListFiles("*.mxd"):   #linked to where workspace is set # keep 1 mxd in folder
   print mappath + mxdfile
   mxd = arcpy.mapping.MapDocument(mappath + mxdfile)
   
   df = arcpy.mapping.ListDataFrames(mxd)
   #print df
   lyr = arcpy.mapping.ListLayers(mxd)
   #print lyr
   #Structures
   #schlyr = arcpy.mapping.ListLayers(mxd,'schools')
   #feat_class = "schools.shp" - based on workspace - shapefile
   #feat_layer = "Schools" - based on workspace - layer
   #hosplyr = arcpy.mapping.ListLayers(mxd, 'hospital')
   #polyr = arcpy.mapping.ListLayers(mxd, 'police')

   #feat_class = "schools.shp" - based on workspace - shapefile
   

   #100
   #x1001shp = r'T:\03Comprehensive_Planning\Environmental\Sustainability\Disaster Preparedness and Planning Project (DP3)\DP3 Charts and Maps\moguam\HAZUS\ken\kml\100yearhazus.shp'
   #x100lyr = arcpy.mapping.ListLayers(mxd,'100 Year*')
   #print x100lyr
#500 +3
   #x5003lyr = arcpy.mapping.ListLayers(mxd,'500 Year + 3*')
   #print x5003lyr
   #allFrames = arcpy.mapping.ListDataFrames(mxd)

   #Fieldnames
   fn100 = "f_100"
   fn500 = "f_500"
   fn5003 = "f_500_3"
   fn5005 = "f_500_5"
   fn5007 = "f_500_7"
   fid = "FID"
####Save each as a new shapefile    ##### 1
   ####export data to new shapefile, add to table of contents same mxd, refresh? 2
####for now will manually list them, future go through list of layers list automatically  #####??? 3


#get access to correct layers in group layer, list them: 
   for dataFrame in df:          #loop dataframes
     #mxd.activeView=dataFrame
     for mapLayers in lyr:      #loop through layers

        ####100 Year
        x100lyr = arcpy.mapping.ListLayers(mxd,'100 Year*') #layer
        for x100lyr in arcpy.mapping.ListLayers(mxd,'100 Year*'):
        #need to just say the layer name
            #print x5003lyr.name
     
           if mapLayers.isGroupLayer and mapLayers.name == "Structure": #a layer can be a group layer
               print 'Group Layer name: ' + mapLayers.name
               print '100 Year - List of layers in Group:'
               for glyr in arcpy.mapping.ListLayers(mapLayers):
                       if glyr != mapLayers:
                           slyr = arcpy.mapping.ListLayers(glyr)
               #if slyr != mapLayers:
                           print 'start'
                           print slyr
                           for slyr in arcpy.mapping.ListLayers(glyr):
                              arcpy.AddField_management(slyr, fn100, "SHORT")   #close arcgis and python before

                              #create list of shapefiles
                              feat_class = shppath + slyr.name + '.shp'
                              print feat_class

                              #select points that intersect flood plain (point shape, point layer)
                              arcpy.MakeFeatureLayer_management(feat_class, slyr.name) #optional?
                              arcpy.SelectLayerByLocation_management(slyr.name, "INTERSECT", x100lyr)

                              #Open a search cursor on structure point layer selected
                              #Gets a collection of rows from feature class/point
                              srows = arcpy.SearchCursor(slyr.name)

                              srow = srows.next()

                              #Print id and extent number value of all the structure points selected
                              while srow:         #while row exists in the cursor
                                 print "FID: " + str(srow.getValue(fid))
                                 srow = srows.next()

                                 #create the update cursor and move cursor to first row
                                 urows = arcpy.UpdateCursor(slyr.name)
                                 urow = urows.next()

###update                        #update row and move to next row if rows are left
                                 while urow:
                                    urow.setValue(fn100, "1")
                                    urows.updateRow(urow)
                                    urow = urows.next()
                                 del urow
                                 del urows
            

                              #Clean up cursor and row objects
                              del srow
                              del srows


                            
                             #print number of selected points in flood plain
                              result = arcpy.GetCount_management(slyr.name)
                              print "Number of selected points in " + slyr.name + ": " + str(result) + " in flood extent: " +  x100lyr.name + "\n \n"

                              arcpy.Delete_management(slyr.name)
                              
      
    ######500 Year
        x500lyr = arcpy.mapping.ListLayers(mxd,'500 Year') #layer
        for x500lyr in arcpy.mapping.ListLayers(mxd,'500 Year'):
        #need to just say the layer name
            #print x5003lyr.name
     
           if mapLayers.isGroupLayer and mapLayers.name == "Structure": #a layer can be a group layer
               print 'Group Layer name: ' + mapLayers.name
               print '500 Year - List of layers in Group:'
               for glyr in arcpy.mapping.ListLayers(mapLayers):
                       if glyr != mapLayers:
                           slyr = arcpy.mapping.ListLayers(glyr)
               #if slyr != mapLayers:
                           print 'start'
                           print slyr
                           for slyr in arcpy.mapping.ListLayers(glyr):
                              arcpy.AddField_management(slyr, fn500, "SHORT")   #close arcgis and python before

                              #create list of shapefiles
                              feat_class = shppath + slyr.name + '.shp'
                              #feat_class1 = mappath + slyr.name + '.shp'
                              print feat_class

                              #select points that intersect flood plain (point shape, point layer)
                              arcpy.MakeFeatureLayer_management(feat_class, slyr.name) #optional?
                              arcpy.SelectLayerByLocation_management(slyr.name, "INTERSECT", x500lyr)

                              #Open a search cursor on structure point layer selected
                              #Gets a collection of rows from feature class/point
                              srows = arcpy.SearchCursor(slyr.name)

                              srow = srows.next()

                              #Print id and extent number value of all the structure points selected
                              while srow:         #while row exists in the cursor
                                 print "FID: " + str(srow.getValue(fid))
                                 srow = srows.next()

                                 #create the update cursor and move cursor to first row
                                 urows = arcpy.UpdateCursor(slyr.name)
                                 urow = urows.next()

                                 #update row and move to next row if rows are left
                                 while urow:
                                    urow.setValue(fn500, "2")
                                    urows.updateRow(urow)
                                    urow = urows.next()
                                 del urow
                                 del urows
            

                              #Clean up cursor and row objects
                              del srow
                              del srows
                            
                             #print number of selected points in flood plain
                              result = arcpy.GetCount_management(slyr.name)
                              print "Number of selected points in " + slyr.name + ": " + str(result) + " in flood extent: " +  x500lyr.name + "\n \n"

                              arcpy.Delete_management(slyr.name)
                              
#####500 +3
        x5003lyr = arcpy.mapping.ListLayers(mxd,'500 Year + 3*')
        for x5003lyr in arcpy.mapping.ListLayers(mxd,'500 Year + 3*'):
        #need to just say the layer name
            #print x5003lyr.name
     
           if mapLayers.isGroupLayer and mapLayers.name == "Structure": #a layer can be a group layer
               print 'Group Layer name: ' + mapLayers.name
               print '500 Year + 3 FT - List of layers in Group:'
               for glyr in arcpy.mapping.ListLayers(mapLayers):
                       if glyr != mapLayers:
                           slyr = arcpy.mapping.ListLayers(glyr)
               #if slyr != mapLayers:
                           print 'start'
                           print slyr
                           for slyr in arcpy.mapping.ListLayers(glyr):
                              arcpy.AddField_management(slyr, fn5003, "SHORT")   #close arcgis and python before

                              #create list of shapefiles
                              feat_class = shppath + slyr.name + '.shp'
                              #feat_class1 = mappath + slyr.name + '.shp'
                              print feat_class

                              #select points that intersect flood plain (point shape, point layer)
                              arcpy.MakeFeatureLayer_management(feat_class, slyr.name) #optional?
                              arcpy.SelectLayerByLocation_management(slyr.name, "INTERSECT", x5003lyr)

                              #Open a search cursor on structure point layer selected
                              #Gets a collection of rows from feature class/point
                              srows = arcpy.SearchCursor(slyr.name)

                              srow = srows.next()

                              #Print id and extent number value of all the structure points selected
                              while srow:         #while row exists in the cursor
                                 print "FID: " + str(srow.getValue(fid))
                                 srow = srows.next()

                                 #create the update cursor and move cursor to first row
                                 urows = arcpy.UpdateCursor(slyr.name)
                                 urow = urows.next()

                                 #update row and move to next row if rows are left
                                 while urow:
                                    urow.setValue(fn5003, "3")
                                    urows.updateRow(urow)
                                    urow = urows.next()
                                 del urow
                                 del urows
            

                              #Clean up cursor and row objects
                              del srow
                              del srows
                            
                             #print number of selected points in flood plain
                              result = arcpy.GetCount_management(slyr.name)
                              print "Number of selected points in " + slyr.name + ": " + str(result) + " in flood extent: " +  x5003lyr.name + "\n \n"

                              arcpy.Delete_management(slyr.name)

####500 + 5
        x5005lyr = arcpy.mapping.ListLayers(mxd,'500 Year + 5*')
        for x5005lyr in arcpy.mapping.ListLayers(mxd,'500 Year + 5*'):
        #need to just say the layer name
            #print x5003lyr.name
     
           if mapLayers.isGroupLayer and mapLayers.name == "Structure": #a layer can be a group layer
               print 'Group Layer name: ' + mapLayers.name
               print '500 Year + 5 FT - List of layers in Group:'
               for glyr in arcpy.mapping.ListLayers(mapLayers):
                       if glyr != mapLayers:
                           slyr = arcpy.mapping.ListLayers(glyr)
               #if slyr != mapLayers:
                           print 'start'
                           print slyr
                           for slyr in arcpy.mapping.ListLayers(glyr):
                              arcpy.AddField_management(slyr, fn5005, "SHORT")   #close arcgis and python before

                              #create list of shapefiles
                              feat_class = shppath + slyr.name + '.shp'
                              #feat_class1 = mappath + slyr.name + '.shp'
                              print feat_class

                              #select points that intersect flood plain (point shape, point layer)
                              arcpy.MakeFeatureLayer_management(feat_class, slyr.name) #optional?
                              arcpy.SelectLayerByLocation_management(slyr.name, "INTERSECT", x5005lyr)

                              #Open a search cursor on structure point layer selected
                              #Gets a collection of rows from feature class/point
                              srows = arcpy.SearchCursor(slyr.name)

                              srow = srows.next()

                              #Print id and extent number value of all the structure points selected
                              while srow:         #while row exists in the cursor
                                 print "FID: " + str(srow.getValue(fid))
                                 srow = srows.next()

                                 #create the update cursor and move cursor to first row
                                 urows = arcpy.UpdateCursor(slyr.name)
                                 urow = urows.next()

                                 #update row and move to next row if rows are left
                                 while urow:
                                    urow.setValue(fn5005, "4")
                                    urows.updateRow(urow)
                                    urow = urows.next()
                                 del urow
                                 del urows
            

                              #Clean up cursor and row objects
                              del srow
                              del srows
                            
                             #print number of selected points in flood plain
                              result = arcpy.GetCount_management(slyr.name)
                              print "Number of selected points in " + slyr.name + ": " + str(result) + " in flood extent: " +  x5005lyr.name + "\n \n"

                              arcpy.Delete_management(slyr.name)


####500 + 7
        x5007lyr = arcpy.mapping.ListLayers(mxd,'500 Year + 7*')
        for x5007lyr in arcpy.mapping.ListLayers(mxd,'500 Year + 7*'):
        #need to just say the layer name
            #print x5003lyr.name
     
           if mapLayers.isGroupLayer and mapLayers.name == "Structure": #a layer can be a group layer
               print 'Group Layer name: ' + mapLayers.name
               print '500 Year + 7 FT - List of layers in Group:'
               for glyr in arcpy.mapping.ListLayers(mapLayers):
                       if glyr != mapLayers:
                           slyr = arcpy.mapping.ListLayers(glyr)
               #if slyr != mapLayers:
                           print 'start'
                           print slyr
                           for slyr in arcpy.mapping.ListLayers(glyr):
                              arcpy.AddField_management(slyr, fn5007, "SHORT")   #close arcgis and python before

                              #create list of shapefiles
                              feat_class = shppath + slyr.name + '.shp'
                              #feat_class1 = mappath + slyr.name + '.shp'
                              print feat_class

                              #select points that intersect flood plain (point shape, point layer)
                              arcpy.MakeFeatureLayer_management(feat_class, slyr.name) #optional?
                              arcpy.SelectLayerByLocation_management(slyr.name, "INTERSECT", x5007lyr)

                              #Open a search cursor on structure point layer selected
                              #Gets a collection of rows from feature class/point
                              srows = arcpy.SearchCursor(slyr.name)

                              srow = srows.next()

                              #Print id and extent number value of all the structure points selected
                              while srow:         #while row exists in the cursor
                                 print "FID: " + str(srow.getValue(fid))
                                 srow = srows.next()

                                 #create the update cursor and move cursor to first row
                                 urows = arcpy.UpdateCursor(slyr.name)
                                 urow = urows.next()

                                 #update row and move to next row if rows are left
                                 while urow:
                                    urow.setValue(fn5007, "5")
                                    urows.updateRow(urow)
                                    urow = urows.next()
                                 del urow
                                 del urows
            

                              #Clean up cursor and row objects
                              del srow
                              del srows
                            
                             #print number of selected points in flood plain
                              result = arcpy.GetCount_management(slyr.name)
                              print "Number of selected points in " + slyr.name + ": " + str(result) + " in flood extent: " +  x5007lyr.name + "\n \n"

                              arcpy.Delete_management(slyr.name)


   del mxd
   print '\n Done'
#-then do the multiple export to dbf
   
#open files in excel manually
