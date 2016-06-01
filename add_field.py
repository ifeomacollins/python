# Name: add_field.py
# Description: add  new field created in unzipped shapefile
#author: Ifeoma Collins
#Date: May 9, 2016


# Import system modules
import arcpy, os, glob

# Set folders for input and output
shapefile_folder = r"M:\unzipped"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = shapefile_folder


#array to store list of all unzipped shapefiles that need to be to have new field added and populated
shpfilearray = []

counter = 0

#access shapefiles in folder
os.chdir(shapefile_folder)
print "Adding shapefiles to array"

#set the field name
field_name = "st_cty"

#find shapefiles in folder and add them to array
for file_name in glob.glob("*.shp"):
    counter = counter + 1
    print counter
    state_county_code = file_name.split("_")[2]  #only get part of file name for state county code
    shpfilearray.append(state_county_code)
    #add a new field to all shapefiles in array as string
    arcpy.AddField_management(file_name, field_name, "TEXT")

print shpfilearray
#print counter



'''
Split notes
i = a.split("_", 1)
only split the first one before the _,
2 means only split the first 2 before the _, and so on..
i[2] - get the third item in the split...
i = a.split("_")
i[2]
'''
del file_name

#print "All " + str(counter) + " shapefiles have the new field created with their file name in corresponding rows."
print '\n Done'
