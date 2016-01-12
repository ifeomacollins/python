'''
Tool Name: Growth Model Look Up Table for Non-TAZ counties (ES and West) and Southern MD and Baco
Source Name: LookUpTableNonTaz.py
Version: ArcGIS 10.2.1 / Python 2.7.5
Author: Melissa Oguamanam, IT Programmer Analyst 2, Maryland Department of Planning
Start Date: April 15, 2015
Finished Date: April 2015
Updated On: July 9 2015 - added Baltimore County
Description:2040 NHA Projections based on (1990-2010 year built) parcel points and census block group geography for Non-TAZ and Southern MD counties and Baco
Required Arguments: Must select a county from the drop down list. Must be using the part1_blockgroup.mxd and have it open with the default layers uploaded.
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


#access the part1_blockgroup.mxd
#shapefile name is not case sensitive
mxd = arcpy.mapping.MapDocument("CURRENT")
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

cbg = arcpy.mapping.ListLayers(mxd, "census*")[0]

#folders

#census folder path
cbg_shppath = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\scripts\data' + "\\"

#output folders
outputPre = r'J:\GIS_WORK\CMP_WORK_Area\MelOgu\growthmodel\scripts\toolboxes\output' + "\\"
#county name2012 + lookup table
outputPostLU = r'\lookup' + "\\"
nontaz = r'K:\Planning Data Analysis\Policy Analysis\Internal\Growth Model\New_Growth Lookup\nontaz_counties' + "\\"

try:
    arcpy.AddMessage("\nYou selected " + countyInput + " County.\n")
    arcpy.AddMessage("\nNow Starting the Growth Look Up Table Code for " + countyInput + " County...\n")

    #do else ifs for county value
    #set county2012 variable based on county name
    #census block query number
    #nha projection number

    #### All Counties
    
    #alle
    if countyInput == alle:
        county = alleLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'24001%\' '   #should be 54
        #parcel points query number is 2484
        proj2040 = 2425
        
    #wash
    elif countyInput == wash:
        county = washLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'24043%\' '   #should be 95
        proj2040 = 17925
        #parcel points query number is 13674
        
    #garr
    elif countyInput == garr:
        county = garrLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'24023%\' '  #should be 22
        proj2040 = 1600
        #parcel points query number is 5225


    #caro
    elif countyInput == caro:
        county = caroLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'24011955%\' '  #should be 23
        proj2040 = 5000
        #parcel points query number is 3533

    #ceci
    elif countyInput == ceci:
        county = ceciLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'240150%\' '  #should be 57
        proj2040 = 16000
        #parcel points query number is 12596

    #kent
    elif countyInput == kent:
        county = kentLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2402995%\' '  #should be 19
        proj2040 = 2500
        #parcel points query number is 2470
        
    #quee
    elif countyInput == quee:
        county = queeLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'240358%\' '  #should be 25
        proj2040 = 8300
        #parcel points query number is 7119

    #talb
    elif countyInput == talb:
        county = talbLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2404196%\' '  #should be 32 or 27?
        proj2040 = 3650
        #parcel points query number is 5613

    #dorc
    elif countyInput == dorc:
        county = dorcLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2401997%\' '  #should be 29
        proj2040 = 3850
        #parcel points query number is 3513

    #some
    elif countyInput == some:
        county = someLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'240399%\' '  #should be 19
        proj2040 = 900
        #parcel points query number is 2322

    #worc
    elif countyInput == worc:
        county = worcLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'240479%\' '  #should be 47
        proj2040 = 6500
        #parcel points query number is 16389

    #wico
    elif countyInput == wico:
        county = wicoLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'240450%\' '  #should be 71
        proj2040 = 12425
        #parcel points query number is 9955

    #calv
    elif countyInput == calv:
        county = calvLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2400986%\' '  #should be 44
        proj2040 = 7250
        #parcel points query number is 14745

        
    #char
    elif countyInput == char:
        county = charLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2401785%\' '  #should be 80
        proj2040 = 32050
        #parcel points query number is 20435
        
    #stma
    elif countyInput == stma:
        county = stmaLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'2403787%\' '  #should be 55
        proj2040 = 24825
        #parcel points query number is 14960

    #baco
    elif countyInput == baco:
        county = bacoLyr
        cbgQ = ' "GEOGRAPHY" LIKE \'24005%\' '  #should be 528
        proj2040 = 40450
        #parcel points query number is 14960

    else:
        arcpy.AddMessage("No proper county selected. The code will break.\n")
    

    arcpy.AddMessage("Name of shapefile being used is " + county.name + ".shp\n")
    arcpy.AddMessage("Its Census Block Group numbers query will be " + cbgQ + "\n")
    arcpy.AddMessage("Its projected household number change in growth for 2040 is " + str(proj2040) + ".\n")


    ##### then do 
    #1. Select census block groups that match query number set above for the right county
    #cbg_feat_class = cbg_shppath + cbg.name + '.shp'
    #arcpy.MakeFeatureLayer_management(cbg_feat_class, cbg.name)  #Need this step
    arcpy.SelectLayerByAttribute_management(cbg.name, "NEW_SELECTION", cbgQ )

    #print number of selected points in Census Block Group
    cresult = arcpy.GetCount_management(cbg.name)
    arcpy.AddMessage("The Number of selected census block groups is " + str(cresult) + " for " + countyInput + " County." + "\n")

    #2. Select the parcel points in the selected county that meet the year built/lu/acres query
    arcpy.SelectLayerByAttribute_management(county.name, "NEW_SELECTION", ' "YEARBLT" >= \'1990\' AND "YEARBLT" <= \'2010\' AND ( "LU" = \'A\' OR "LU"= \'R\' OR "LU"=\'TH\' OR "LU" = \'U\') AND "ACRES" <= 20 AND "NFMIMPVL" >= 10000')
    #print number of selected points in Census Block Group
    presult = arcpy.GetCount_management(county.name)
    arcpy.AddMessage("Number of selected parcels in " + county.name + " is " + str(presult) + ".\n")

    #3. Field Mappings
    targetFeatures = cbg.name
    joinFeatures = county.name
    outfc = outputPre + county.name + outputPostLU
    fieldmappings = arcpy.FieldMappings() #create FieldMappings Object
    fieldmappings.addTable(targetFeatures) #then add tables that are to be combined
    fieldmappings.addTable(joinFeatures)

    #getAcctID
    acctidFieldIndex = fieldmappings.findFieldMapIndex("ACCTID")
    fieldmap = fieldmappings.getFieldMap(acctidFieldIndex)

    #set merge rule Count
    fieldmap.mergeRule = "count"
    fieldmappings.replaceFieldMap(acctidFieldIndex, fieldmap)
    arcpy.AddMessage("Field Mapping done")

    #4. Spatial Join selected Census Blocks to selected parcel points by AcctID completely inside block group
    #matching
    match_option = "COMPLETELY_CONTAINS"
    arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outfc + "joined_" + cbg.name + "_" + county.name, "#", "#", fieldmappings, match_option)
    arcpy.AddMessage("Spatial Join done")


    #Using newly created spatially joined shapefile... named based on county name
    inFeatures = outfc + "joined_" + cbg.name + "_" + county.name + ".dbf"
    print inFeatures
            
    #5. Populate Recent Growth Field
    fieldName = "RECENTGROW"
    expression = '!Join_Count!'
    arcpy.CalculateField_management(inFeatures, fieldName, expression, "PYTHON_9.3")
    arcpy.AddMessage("Join Count numbers added to Recent Growth Field")

    #Need sum of recent growth...
    arr = arcpy.da.FeatureClassToNumPyArray(inFeatures, ('RECENTGROW'))

    # Sum the total population between 1990 and 2010
    rg_sum = arr["RECENTGROW"].sum()
    arcpy.AddMessage("The total sum of features in Recent Growth is: " + str(rg_sum))

    #6. Populate Percent Growth Field
    fieldName2 = "PCTGROWTH"
    arcpy.CalculateField_management(inFeatures, fieldName2, "(float('!RECENTGROW!')) / " +  str(rg_sum), "PYTHON_9.3")
    arr = arcpy.da.FeatureClassToNumPyArray(inFeatures, ('PCTGROWTH'))
    pct_sum = arr["PCTGROWTH"].sum()
    arcpy.AddMessage("The total sum of features in PCT Growth is: " + str(pct_sum))  #The sum needs to be 1, not 100.

    #7. Populate NHA Field. Use NHA projection number picked from above
    fieldName3 = "NHA"
    expression3 = "float('!PCTGROWTH!') *" + str(proj2040)
    arcpy.CalculateField_management(inFeatures, fieldName3, expression3, "PYTHON_9.3")
    arr = arcpy.da.FeatureClassToNumPyArray(inFeatures, ('NHA'))
    nha_sum = arr["NHA"].sum()
    arcpy.AddMessage("The total sum of features in NHA is: " + str(nha_sum))

    #8. Remove excess fields
    desc = arcpy.Describe(inFeatures)
    # Use ListFields to get a list of field objects
    fieldObjList = arcpy.ListFields(inFeatures)
    fieldnames = [f.name for f in arcpy.ListFields(inFeatures)]
    print "List of All Fields"
    print fieldnames
    print "\n \n"
    # Create an empty list that will be populated with field names to be removed        
    fieldNameList = []
    #for each field in the object list add field name to the list if it does not equal
    #FID, Shape*, Join_Count, GEOGRAPHY, recentgrowth, pctgrowth, nha, JURSCODE
    for field in fieldObjList:
        #here
        if field.name != "GEOGRAPHY" and field.name !="Join_Count" and field.name !="FID" and field.name !="Shape" and field.name !="NHA" and field.name !="RECENTGROW" and field.name !="JURSCODE" and field.name !="PCTGROWTH":
            #here
            fieldNameList.append(field.name)
    #print fieldNameList
    arcpy.AddMessage("List of Fields that will be removed made.")
    print fieldNameList

    # Set local variables
    inTable = inFeatures                    
    dropFields = fieldNameList
    # Execute DeleteField
    arcpy.DeleteField_management(inTable, dropFields)    
    arcpy.AddMessage("Excess fields removed from joined shapefile.\n")

    #9. add all final dbfs to a non-taz folder that steph sent. just dbfs
    env.workspace = outfc 
    for dbffile in arcpy.ListFiles("*.dbf"):  #list all dbfs in folder
        #arcpy.AddMessage(outfc + dbffile)
        dbf = outfc + dbffile
        #shutil.copyfile(dbf, outputPre)
        #arcpy.AddMessage("Done adding dbf to non-tax folder")
        #rename countygrowth.dbf


    del cbg, alleLyr, garrLyr, washLyr, mxd
    
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
