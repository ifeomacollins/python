# Name: addfilename_to_field.py
# Description: add the corresponding file name to new field created in unzipped shapefile
#author: Ifeoma Collins
#Date: May 9, 2016


# Import system modules
import arcpy, os, glob

# Set folders for input and output
shapefile_folder = r"M:\\unzipped" + "\\"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = shapefile_folder

#array to store list of all unzipped shapefiles that need to be to have new field added and populated
shpfilearray = []

counter = 0

#access shapefiles in folder
os.chdir(shapefile_folder)
print "Accessing shapefiles in folder to update field values"

#set the field name
field_name = "st_cty"
field = ['st_cty']

#find shapefiles in folder and add them to array
for file_name in glob.glob("*.shp"):
    counter = counter + 1
    print counter
    state_county_code = file_name.split("_")[2]  #only get part of file name for state county code

    #break file name into parts
    state_county_fc = shapefile_folder + file_name
    #print state_county_fc
    
    #turn file_name into a feature class
    arcpy.MakeFeatureLayer_management(state_county_fc, file_name.strip(".shp"))
    
    #create inTable variable
    inTable = state_county_fc

    #create urows variable
    urows = arcpy.da.UpdateCursor(inTable,["st_cty"])

    #urow for loop
    for urow in urows:
        urow[0] = state_county_code
        urows.updateRow(urow)
    #set urow value for right field

    #update urow


del file_name, urow, urows

print "All " + str(counter) + " shapefiles have the new field populated with their file name in corresponding rows."
print '\n Done'
