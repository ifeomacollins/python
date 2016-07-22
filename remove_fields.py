# Name: remove_fields.py
# Description: Delete several fields from a feature class  and only keep
#geodatabased fields like objectid, shapearea, ....
#author: Ifeoma Collins
#Date: May 2, 2016


# Import system modules
import arcpy


# Set environment settings
arcpy.env.workspace = r"M:\icollins"

#folders
mxdpath = r"M:\icollins" + "\\"

dbpath = r"M:\database.gdb" + "\\"
 
for mxdfile in arcpy.ListFiles("*.mxd"):   #linked to where workspace is set
    print mxdpath + mxdfile
    mxd = arcpy.mapping.MapDocument(mxdpath + mxdfile)
    df = arcpy.mapping.ListDataFrames(mxd)
    lyr = arcpy.mapping.ListLayers(mxd)
    #print lyr

    #access different layers in mxd
    blockgroup__lyr = arcpy.mapping.ListLayers(mxd, "BlockGroup")


    #loop through every layer in dataframe #get access to correct layers
    for dataFrame in df:          #loop dataframes
        for blockgroup in blockgroup_lyr:
            print blockgroup

            #access dbf
            inFeatures = dbpath + "BlockGroup"
            print inFeatures

            #Remove excess fields
            #first get a list of all fields
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
            #OBJECTID, Shape, GEOID, Shape_Length, Shape_Area
            for field in fieldObjList:
                #here
                if field.name != "OBJECTID" and field.name !="Shape" and field.name !="GEOID" and field.name !="Shape" and field.name !="Shape_Length" and field.name !="Shape_Area":
                    
                    fieldNameList.append(field.name)
            print "List of fields to be removed listed below"
            print fieldNameList

            # Set local variables
            inTable = inFeatures                    
            dropFields = fieldNameList
            # Execute DeleteField
            arcpy.DeleteField_management(inTable, dropFields)    
            print "Attribute data fields removed from  feature class.\n"


del mxdfile, mxd
print '\n Done'
