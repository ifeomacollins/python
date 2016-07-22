# Name: alter_field_names.py
# Description: alter perentage fields to begin with pct_ in demographics tables (pct, pm, ph)..
#county, zipcode, state, blockgroup
#author: Ifeoma Collins
#Date: May 6, 2016


# Import system modules
import arcpy
from arcpy import env

# Set folders 
shapefile_folder = r'E:\db.sde'
env.workspace = shapefile_folder

#go to demographics tables (county, blockgroup, state, zipcode) in gdb
datasetList = arcpy.ListTables("*")  #only tables that have demographics at the end

print datasetList

for table in datasetList: #loop through tables
    fieldList = arcpy.ListFields(table)  #get a list of fields for each feature class
    for field in fieldList: #loop through each field
        #print field.name
        string_fn = str(field.name)  
        #print string_fn
        #print "printing field names that begin with pm, ph, or pct and not pct_ and then altering fields"
        #print string_fn.startswith('pm')  #starts with returns true or false
        if string_fn.startswith('pm') == True or string_fn.startswith('ph') == True or (string_fn.startswith('pct') == True and string_fn.startswith('pct_') != True): #doesn't add another pct_ in front of fields that already have it
            print "printing field names that begin with pm, ph, or pct and not pct_ and then altering fields"
            #print string_fn.startswith('pm')  #startswith returns true or false
            print field.name #or field.name == 'pct*' or field.name== 'pm*':
            arcpy.AlterField_management(table, field.name, "pct_" + string_fn) #add pct_ in front of field name

    
        #print "printing field names that begin with pct_"  
        if string_fn.startswith('pct_') == True:
            print "printing field names that begin with pct_"  
            print field.name
        
del table, field
print "\n All percent fields name changed to have pct_ at the beginning."
print '\n Done'
