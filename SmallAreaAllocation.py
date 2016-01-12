'''
Tool Name: Small Area Allocation (Generalized Zoning/Sewer Service Status) for Non-TAZ counties (ES and West) and Southern MD and Baco
Source Name: Small Area Allocation.py
Version: ArcGIS 10.2.1 / Python 2.7.5
Author: Melissa Oguamanam, IT Programmer Analyst 2, Maryland Department of Planning
Start Date: May 20, 2015
Finished Date:
Updated On: July 9 2015
Description: 2040 NHA Small Area Allocation within Generalized Zoning/Sewer areas with census block groups based on parcels built between 1990-2010.
Required Arguments: Must select a county from the drop down list. Must be using the part2_smallarea_zonsew.mxd and have it open with the default layers uploaded.
Optional Arguments: N/A

'''

# Import ArcPy site-package to use Arcgis and os modules to use operating system
import arcpy, os, sys, string, numpy, traceback, shutil #shutil for copying files
from arcpy import env
env.overwriteOutput = True

#get county value from user input
countyInput = arcpy.GetParameterAsText(0)

#variables for each county?
alle = "Allegany"
wash = "Washington"
garr = "Garrett"

caro = "Caroline"
ceci = "Cecil"
kent = "Kent"
quee = "Queen Anne's"
talb = "Talbot"

dorc = "Dorchester"
some = "Somerset"
worc = "Worcester"
wico = "Wicomico"

calv = "Calvert"
char = "Charles"
stma = "St. Mary's"

baco = "Baltimore"

#access the opened part2_smallarea_zonsew.mxd
mxd = arcpy.mapping.MapDocument("CURRENT")

#shapefile name is not case sensitive
#access county parcel point layers
alleLyr = arcpy.mapping.ListLayers(mxd, "Alle*")[0]
washLyr = arcpy.mapping.ListLayers(mxd, "wash*")[0]
garrLyr = arcpy.mapping.ListLayers(mxd, "garr*")[0]

caroLyr = arcpy.mapping.ListLayers(mxd, "caro*")[0]
ceciLyr = arcpy.mapping.ListLayers(mxd, "ceci*")[0]
kentLyr = arcpy.mapping.ListLayers(mxd, "kent*")[0]
queeLyr = arcpy.mapping.ListLayers(mxd, "quee*")[0]
talbLyr = arcpy.mapping.ListLayers(mxd, "talb*")[0]

dorcLyr = arcpy.mapping.ListLayers(mxd, "dorc*")[0]
someLyr = arcpy.mapping.ListLayers(mxd, "some*")[0]
worcLyr = arcpy.mapping.ListLayers(mxd, "worc*")[0]
wicoLyr = arcpy.mapping.ListLayers(mxd, "wico*")[0]

calvLyr = arcpy.mapping.ListLayers(mxd, "calv*")[0]
charLyr = arcpy.mapping.ListLayers(mxd, "char*")[0]
stmaLyr = arcpy.mapping.ListLayers(mxd, "stma*")[0]

bacoLyr = arcpy.mapping.ListLayers(mxd, "baco*")[0]

#census layer
cbg = arcpy.mapping.ListLayers(mxd, "census*")[0]

#zoning layer
gen = arcpy.mapping.ListLayers(mxd, "generalized_zon*")[0]

#sewer layer
sew = arcpy.mapping.ListLayers(mxd, "sewer*")[0]

#folders
#census folder path
cbg_shppath = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\scripts\data' + "\\"

#output folders (lookup)
outputPre = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\scripts\toolboxes\output' + "\\"
#county name2012 + lookup table
outputPostLU = r'\lookup' + "\\"

#output name2012 + zonsew
outputPostZS = r'\zonswr' + "\\"

#dissolved data folder for gen zone and sew
diss_output = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\scripts\toolboxes\int_data\dissolve' + "\\"

#union folder for cbg and dissolved gen zone and sew
diss_union = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\scripts\toolboxes\int_data\union' + "\\"

#folder for steph##############
#nontaz = r'K:\Planning Data Analysis\Policy Analysis\Internal\Growth Model\New_Growth Lookup\nontaz_counties' + "\\"


try:
    arcpy.AddMessage("\nYou selected " + countyInput + " County.\n")
    arcpy.AddMessage("\nNow Starting the Small Area Location (Zoning/Sewer) for " + countyInput + " County...\n")

    #### All Counties
    
    #alle
    if countyInput == alle:
        county = alleLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'24001%\' '   #should be 54
        #parcel points query number is 2484
        proj2040 = 2425
        jurscode = "ALLE"
        
    #wash
    elif countyInput == wash:
        county = washLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'24043%\' '   #should be 95
        proj2040 = 17925
        #parcel points query number is 13674
        jurscode = "WASH"
        
    #garr
    elif countyInput == garr:
        county = garrLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'24023%\' '  #should be 22
        proj2040 = 1600
        #parcel points query number is 5225
        jurscode = "GARR"


    #caro
    elif countyInput == caro:
        county = caroLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'24011955%\' '  #should be 23
        proj2040 = 5000
        #parcel points query number is 3533
        jurscode = "CARO"

    #ceci
    elif countyInput == ceci:
        county = ceciLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'240150%\' '  #should be 57
        proj2040 = 16000
        #parcel points query number is 12596
        jurscode = "CECI"

    #kent
    elif countyInput == kent:
        county = kentLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2402995%\' '  #should be 19
        proj2040 = 2500
        #parcel points query number is 2470
        jurscode = "KENT"
        
    #quee
    elif countyInput == quee:
        county = queeLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'240358%\' '  #should be 25
        proj2040 = 8300
        #parcel points query number is 7119
        jurscode = "QUEE"

    #talb
    elif countyInput == talb:
        county = talbLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2404196%\' '  #should be 32 or 27?
        proj2040 = 3650
        #parcel points query number is 5613
        jurscode = "TALB"

    #dorc
    elif countyInput == dorc:
        county = dorcLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2401997%\' '  #should be 29
        proj2040 = 3850
        #parcel points query number is 3513
        jurscode = "DORC"

    #some
    elif countyInput == some:
        county = someLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'240399%\' '  #should be 19
        proj2040 = 900
        #parcel points query number is 2322
        jurscode = "SOME"

    #worc
    elif countyInput == worc:
        county = worcLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'240479%\' '  #should be 47
        proj2040 = 6500
        #parcel points query number is 16389
        jurscode = "WORC"

    #wico
    elif countyInput == wico:
        county = wicoLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'240450%\' '  #should be 71
        proj2040 = 12425
        #parcel points query number is 9955
        jurscode = "WICO"

    #calv
    elif countyInput == calv:
        county = calvLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2400986%\' '  #should be 44
        proj2040 = 7250
        #parcel points query number is 14745
        jurscode = "CALV"

        
    #char
    elif countyInput == char:
        county = charLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2401785%\' '  #should be 80
        proj2040 = 32050
        #parcel points query number is 20435
        jurscode = "CHAR"
        
    #stma
    elif countyInput == stma:
        county = stmaLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2403787%\' '  #should be 55
        proj2040 = 24825
        #parcel points query number is 14960
        jurscode = "STMA"

    #baco
    elif countyInput == baco:
        county = bacoLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'24005%\' '  #should be 55
        proj2040 = 40450
        #parcel points query number is 14960
        jurscode = "BACO"

    else:
        arcpy.AddMessage("No proper county selected. The code will break.\n")
    

    arcpy.AddMessage("Name of shapefile being used is " + county.name + ".shp\n")
    arcpy.AddMessage("Its Census Block Group numbers query will be " + cbgQ + "\n")
    arcpy.AddMessage("Its projected household number change in growth for 2040 is " + str(proj2040) + ".\n")

    #part 1
    #select census block group query for county
    #1. Select census block groups that match query number set above for the right county
    #cbg_feat_class = cbg_shppath + cbg.name + '.shp'
    arcpy.SelectLayerByAttribute_management(cbg.name, "NEW_SELECTION", cbgQ )

    #print number of selected points in Census Block Group
    cresult = arcpy.GetCount_management(cbg.name)
    arcpy.AddMessage("The Number of selected census block groups is " + str(cresult) + " for " + countyInput + " County." + "\n")
    
    #select parcel points that meet query
    #2. Select the parcel points in the selected county that meet the year built/lu/acres query
    arcpy.SelectLayerByAttribute_management(county.name, "NEW_SELECTION", ' "YEARBLT" >= \'1990\' AND "YEARBLT" <= \'2010\' AND ( "LU" = \'A\' OR "LU"= \'R\' OR "LU"=\'TH\' OR "LU" = \'U\') AND "ACRES" <= 20 AND "NFMIMPVL" >= 10000')
    #print number of selected points in Census Block Group
    presult = arcpy.GetCount_management(county.name)
    arcpy.AddMessage("Number of selected parcels in " + county.name + " is " + str(presult) + ".\n")

    #3. select gen zone layers with zone that has county name
    arcpy.SelectLayerByAttribute_management(gen.name, "NEW_SELECTION", ' "JURSCODE" = \'' + jurscode + '\' ' )
    #print number of selected points in Gen Zone. Wico is 1870 results
    gresult = arcpy.GetCount_management(gen.name)
    arcpy.AddMessage("Number of selected zone features in " + gen.name + ": " + str(gresult) + "for " + countyInput + "\n \n")

    #dissolve gen zone to ??layer a new layer to just genzone field for that county
    #save to dissolve folder
    arcpy.Dissolve_management(gen.name, diss_output + "diss_" + gen.name + "_" + county.name, "GENZONE")
    arcpy.AddMessage("Done Dissolving MD Gen Zone")
    diss_gen = diss_output + "diss_" + gen.name + "_" + county.name + '.shp'
    g_diss_result = arcpy.GetCount_management(diss_gen)
    arcpy.AddMessage("Number of rows dissolved in MD genzone is " + str(g_diss_result) + "\n \n")
                     
    #select sewer zone that has county name
    arcpy.SelectLayerByAttribute_management(sew.name, "NEW_SELECTION", ' "JURSCODE" = \'' + jurscode + '\' ' )
    #print number of selected points in Sew. Should  be 1409
    sresult = arcpy.GetCount_management(sew.name)
    arcpy.AddMessage("Number of selected features in " + sew.name + ": " + str(sresult) + " for " + countyInput + "\n \n")
                       
    #dissolve sewer layer  ??layer to just genz_swr field
    #save to dissolve folder
    arcpy.Dissolve_management(sew.name, diss_output + "diss_" + sew.name + "_" + county.name, "GENZ_SWR")
    arcpy.AddMessage("Done Dissolving MD Sewer Service")
    diss_sew = diss_output + "diss_" + sew.name + "_" + county.name + '.shp'
    s_diss_result = arcpy.GetCount_management(diss_sew)
    arcpy.AddMessage("Number of rows dissolved in MD sewer service is " + str(s_diss_result) + "\n \n")
    
    #union of census block group layer ??layer,  dissolved gen zone, dissolved sewer - makes a shapefile
    #union cbg, and diss genzone and diss swr
    un_in = [cbg.name, diss_gen, diss_sew]
    un_out = diss_union + "diss_cbg_gen_sew_" + county.name + '.shp'  
    arcpy.Union_analysis (un_in, un_out)
    arcpy.AddMessage("Union of CGB and Dissolved Gen and Sewer Done")

    
    #dissolve the union based on geography, genzone, genswr fields
    #dissolve above shapefile based on geoid, genzone, and swr
    arcpy.Dissolve_management(diss_union + "diss_cbg_gen_sew_" + county.name + '.shp', diss_output + "diss_un_cgb_gen_sew" + "_" + county.name, ["GEOGRAPHY", "GENZONE", "GENZ_SWR"])
    arcpy.AddMessage("Dissolve of Union of CGB and Dissolved Gen and Sewer Done")
                       
    #spatial join selected points to above dissolved union
    targetFeatures = diss_output + "diss_un_cgb_gen_sew" + "_" + county.name + '.shp'
    joinFeatures = county.name
    outfc = outputPre + county.name + outputPostZS

    #fieldmapping
    fieldmappings = arcpy.FieldMappings() #create FieldMappings Object
    fieldmappings.addTable(targetFeatures) #then add tables that are to be combined
    fieldmappings.addTable(joinFeatures)

    #getAcctID from parcel shapefile
    acctidFieldIndex = fieldmappings.findFieldMapIndex("ACCTID")
    fieldmap = fieldmappings.getFieldMap(acctidFieldIndex)

    #set merge rule Count
    fieldmap.mergeRule = "count"
    #replace field map?
    fieldmappings.replaceFieldMap(acctidFieldIndex, fieldmap)

    #spatial join points to above shapefile
    #matching
    match_option = "COMPLETELY_CONTAINS"
                       
    arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outfc + county.name + '_pts_cbg_zon_sew' + '.shp', "#", "#", fieldmappings, match_option)
    arcpy.AddMessage("Finished Spatial Join of Parcel Points to dissolved CGB, zoning, and sewer service" + "\n \n")

    #remove unncessary fields
    #remove unnecessary fields
    updatedTable = outfc + county.name + '_pts_cbg_zon_sew' + '.shp'

    # Describe the input (need to test the dataset and data types)
    desc = arcpy.Describe(updatedTable)

    # Use ListFields to get a list of field objects
    fieldObjList = arcpy.ListFields(updatedTable)
    fieldnames = [f.name for f in arcpy.ListFields(updatedTable)]

    # Create an empty list that will be populated with field names to be removed        
    fieldNameList = []

    #for each field in the object list add field name to the list if it does not equal
    #FID, Shape*, Join_Count, GEOGRAPHY, GENZONE, GENZ_SWR, JURSCODE
    for field in fieldObjList:
        #here
        if field.name != "GEOGRAPHY" and field.name !="GENZONE" and field.name !="FID" and field.name !="Shape" and field.name !="Join_Count" and field.name !="GENZ_SWR" and field.name !="JURSCODE":
            #here
            #print "Fields being removed"
            fieldNameList.append(field.name)

    # Set local variables
    inTable = updatedTable                    
    dropFields = fieldNameList

    # Execute DeleteField
    arcpy.DeleteField_management(inTable, dropFields)
    arcpy.AddMessage("non-essential Fields were removed from spatial join")

    

    ##########part 2
    #add new field cbgtotal and add values to it
    fn1 = "CBGTOTAL"
    f1precision = 9
    arcpy.AddField_management(inTable, fn1, "LONG", 9)
    arcpy.AddMessage("CBGTOTAL field added")

    #for all select geography with the same value, CGBTOTAL = sum of join_count
    #or create an array for all possible values; create a list of all unique field values

    srows = arcpy.SearchCursor(inTable)
    srow = srows.next()
    mylist = []

    while srow: #while a row exists in a cursor
        #here
        geog = srow.GEOGRAPHY
        #add every value in the geography field to the mylist array
        mylist.append(geog)

        #need to store just unique geog values in an array
        srow = srows.next()
        geog_set = set(mylist)

    arcpy.AddMessage("Done search cursor for Geography column")
    #print all unique values in geography column just once
    arcpy.AddMessage(geog_set)

    for i in geog_set:
        #here
        #select by attributes geography equals i
        feat_class = inTable
        feat_layer = county.name + '_pts_cbg_zon_sew'
        arcpy.MakeFeatureLayer_management(feat_class, feat_layer)
        query = "(\"GEOGRAPHY\" = '" + i + "')"
        arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", query )
        arcpy.AddMessage(str(i) + " Geography features selected")
        jcresult = arcpy.GetCount_management(feat_layer)
        arcpy.AddMessage("Number of selected rows " + str(jcresult))
        #sum the join_count column
        inFeatures1 = outfc + feat_layer + ".dbf"
        arr = arcpy.da.FeatureClassToNumPyArray(inFeatures1, ('Join_Count'), query)
        # Sum the join_count for each census block group
        jc_sum = arr["Join_Count"].sum()
        #print i and sum to validate
        arcpy.AddMessage("The total sum of parcel points in Census Block group " + str(i) + " is " + str(jc_sum))

        #make cbgtotal = the sum of join_count for selected features
        arcpy.CalculateField_management(feat_layer, "CBGTOTAL", jc_sum, "PYTHON_9.3")
        arcpy.AddMessage(str(jc_sum) + " sum total added to this geography " + str(i) + " in CBGTOTAL field")
    
        #make a pct growth field
        #make a pct growth field - float
        fn2 = "PCTGROWTH"
        arcpy.AddField_management(inTable, fn2, "FLOAT")
        arcpy.AddMessage("PCT Growth field added")

        #prevent the cbg sum is 0 error
        if jc_sum > 0:
            #
            #make pctgrowth = join_count for selected features / the sum of the join count by cbg
            arcpy.CalculateField_management(feat_layer, "PCTGROWTH", "(float('!Join_Count!') / float('!CBGTOTAL!'))", "PYTHON_9.3")
            arr2 = arcpy.da.FeatureClassToNumPyArray(inFeatures1, ('PCTGROWTH'))
            pct_sum = arr2["PCTGROWTH"].sum()
            arcpy.AddMessage("The total sum of features in PCT Growth is: " + str(pct_sum))  #The sum needs to be 1, not 100.

        else:
            arcpy.AddMessage("0% PCT Growth")

        
    ##table join smallarea shp and joined from part 1 based on geography
    #table join smallarea shp and joined from part 1 based on geography
    #layername - feat_layer
    #go to joined_cenus_blocks_ for county2012 shapefile created from part 1 to get fields geography
    #table join
    arcpy.SelectLayerByAttribute_management(feat_layer, "CLEAR_SELECTION") #so all features wills show
    joinTable = outputPre + county.name + outputPostLU + "joined_" + cbg.name + "_" + county.name + ".dbf" #this should be shapefile created in part 1 with join, geog, recent, pct, and nha
    joinField = "GEOGRAPHY"
    env.qualifiedFieldNames = False  #so outputfield name won't have table name
    arcpy.AddJoin_management(feat_layer, joinField, joinTable, joinField)
    arcpy.AddMessage("Table join based on geography done")

    #create a new shapefile
    copyFeature = outputPre + county.name + outputPostZS + county.name + "_zon_sew_nha"
    arcpy.CopyFeatures_management(feat_layer, copyFeature)
    arcpy.AddMessage("Features copied to a new shapefile")
    
    #remove excess fields
    # Use ListFields to get a list of field objects
    fieldObjList = arcpy.ListFields(copyFeature + '.shp')
    #print fieldObjList

    fieldnames = [f.name for f in arcpy.ListFields(copyFeature + '.shp')]
    arcpy.AddMessage("List of All Fields in zon_sew_nha shapfile")
    arcpy.AddMessage(fieldnames)
    arcpy.AddMessage("\n \n")

    # Create an empty list that will be populated with field names to be removed        
    fieldNameList = []

    #for each field in the object list add field name to the list if it does not equal
    #FID, Shape*, Join_Count, GEOGRAPHY, GENZONE, GENZ_SWR, JURSCODE
    for field in fieldObjList:
        #here
        if field.name != "GEOGRAPHY" and field.name !="Join_Count" and field.name !="FID" and field.name !="Shape" and field.name !="GENZ_SWR" and field.name !="GENZONE" and field.name !="NHA" and field.name !="JURSCODE" and field.name !="PCTGROWTH" and field.name !="CBGTOTAL":
            #here
            #print "Fields being removed"
            fieldNameList.append(field.name)

    #print fieldNameList
    arcpy.AddMessage("List of Fields that will be removed")
    arcpy.AddMessage(fieldNameList)

    # Set local variables
    inTable = copyFeature + '.shp'                   
    dropFields = fieldNameList
                                                           

    # Execute DeleteField
    arcpy.DeleteField_management(inTable, dropFields)
                        
    arcpy.AddMessage("Excess fields removed.")

    
    #make nha_zonsew field = NHA * PCTGROWTH
    #make a nha_zon_sew - long precision 9
    fn3 = "NHA_zonsew"
    arcpy.AddField_management(inTable, fn3, "FLOAT")
    arcpy.AddMessage("NHA zonsew field added")

    #make a new field with the names of values in GENZONE and GENZ_SWR columns
    arcpy.AddField_management(inTable, "ZON_SWR", "TEXT")

    #search through rows.. update cursors ..needs to be synchronized
    #add value of "genzone" and space and "genz_swr" to zone swr field

    #make NHA_zonsew = NHA * PCTGROWTH
    arcpy.CalculateField_management(copyFeature + '.shp', "NHA_zonsew", "float('!PCTGROWTH!') * float('!NHA!')", "PYTHON_9.3")

    ####what is this section for?
    #feat_class =  output + county.name + '_zon_sew_nha' + '.shp'
    #feat_layer = county.name + '_zon_sew_nha'
    #arcpy.MakeFeatureLayer_management(feat_class, feat_layer)
    #inFeatures1 = outfc + feat_layer + ".dbf"
    ###what is this section for?

    #make a concatenated zonsew field
    #search first - get collection of rows from feature class
    srows2 = arcpy.SearchCursor(inTable)

    fid = 0
    zs_list = []

    for srow2 in srows2:
        #assign a variable for the value of srow.getvalue(genzone)
        #assign a variable for the value of srow.getvalue(genz_swr)
        genzone = srow2.getValue("GENZONE")
        genz_swr = srow2.getValue("GENZ_SWR")

        #make query for synchronization
        query = '"FID" = ' + str(fid)
                       
        #cycle through one row because of query to update with values from search cursor
        urows = arcpy.UpdateCursor(inTable, query)
                          
        for urow in urows:
            urow.ZON_SWR = genzone + " " + genz_swr
            zs = urow.ZON_SWR
            zs_list.append(zs)
                                
            urows.updateRow(urow)
            zs_set = set(zs_list)
            
        fid += 1
    del urow, urows, srow2, srows2
    arcpy.AddMessage("Values of Genzone and GENZ SWR concatenated into zone_swr field")
    arcpy.AddMessage(zs_set)

    

except:
    print arcpy.GetMessages(2)
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n     " + str(sys.exc_type) + ": " + str(sys.exc_value) + "\n"
    msgs = "arcpy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    arcpy.AddError(msgs)
    arcpy.AddError(pymsg)

    print msgs
    print pymsg

    arcpy.AddMessage(arcpy.GetMessages(1))
    print arcpy.GetMessages(1)



    


