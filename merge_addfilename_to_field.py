# Name: merge_addfilename_to_field.py.py
# Description: merge all shapefiles in folder and store in file geodatabase. add the corresponding file name to new
#field created
#author: Ifeoma Collins
#Date: May 9, 2016


# Import system modules
import arcpy, os, glob

# Set folders for input and output
shapefile_folder = r"M:\unzipped"
arcpy.env.workspace = shapefile_folder
filegdb = r'M:\db.gdb\addrfeat'

#array to store list of all shapefiles that need to be merged
shpfilearray = []

counter = 0

#access shapefiles in folder
os.chdir(shapefile_folder)
print "Adding shapefiles to array"

#find shapefiles in folder and add them to array
for file in glob.glob("*.shp"):
    counter = counter + 1
    print counter
    shpfilearray.append(file)

#merge shapefiles
arcpy.Merge_management(shpfilearray, filegdb)


del file

print "All " + str(counter) + " shapefiles have been merged into one feature class and stored in a file geodatabase."
print '\n Done'
