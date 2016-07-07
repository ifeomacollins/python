# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# join_service_function.py
# edited by Ifeoma Collins May 25 2016
# Usage: join <Input_Layer> <Input_Join_Field> <CSV_Table> <CSV_Field_for_Join> <Keep_All_Target_Features> <Join_Output> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, traceback, os

# Script parameters
'''
#Get Geography
geography = arcpy.GetParameterAsText(0)

#geog fields
geog_field = arcpy.GetParameterAsText(1)

#csv table
CSV_Table = arcpy.GetParameterAsText(2)

#csv field
CSV_Field_for_Join = arcpy.GetParameterAsText(3)

#keep all features
Keep_All_Target_Features = arcpy.GetParameterAsText(4)

#join output
Join_Output = arcpy.GetParameterAsText(5)
'''

'''
#geography variables
county = 'County'
state = 'State'
zcta = 'ZCTA'
blockgroup = 'Block Group'
condist = 'Congressional District'
puma = 'PUMA'
#zipcode = 'Zip Code'


#us boundaries in sde gdb
#need to register geodatabase
#root = r"E:\sde-db-connections"
#wp = "aarpsql.aarpdev.spatialsys.com as gisent1-owner.sde"
#db = "gisent1.DBO.US_Boundaries"
#gdb = os.path.join(r"E:\sde-db-connections\aarpsql.aarpdev.spatialsys.com as gisent1-owner.sde\gisent1.DBO.US_Boundaries" , "\\")
gdb = r"E:\sde-db-connections\aarpsql.aarpdev.spatialsys.com as gisent1-owner.sde\gisent1.DBO.US_Boundaries" 
#M:\AARP\DevelopmentEnvironment\database-connections\aarpsql.aarpdev.spatialsys.com as gisent1-owner.sde\gisent1.DBO.US_Boundaries
#M:\AARP\DevelopmentEnvironment\database-connections\aarpsql.aarpdev.spatialsys.com as gisent1-owner.sde\gisent1.DBO.US_Boundaries\gisent1.DBO.County_20m
county20_fc = os.path.join(gdb, "gisent1.DBO.County_20m")
state20_fc =  os.path.join(gdb, "gisent1.DBO.State_20m")
zcta_fc = os.path.join(gdb, "gisent1.DBO.ZCTA_500k")
blockgroup_fc = os.path.join(gdb, "gisent1.DBO.BlockGroup_Detailed")
condist_fc = os.path.join(gdb, "gisent1.DBO.ConDist_20m")
puma_fc = os.path.join(gdb, "gisent1.DBO.Puma_500k")
#zipcodedet_fc = gdb + "gisent1.DBO.ZipCode_Detailed"

arcpy.AddMessage(gdb)
arcpy.AddMessage(state20_fc)

'''

#gdb location
#local computer
#gdb = r"M:\AARP\DevelopmentEnvironment\database-connections\aarpsql.aarpdev.spatialsys.com as gisent1-owner.sde"
#gdb_bound = r"M:\AARP\DevelopmentEnvironment\database-connections\aarpsql.aarpdev.spatialsys.com as gisent1-owner.sde\gisent1.DBO.US_Boundaries"
gdb =r"M:\AARP\DevelopmentEnvironment\database-connections"
sde = "aarpsql.aarpdev.spatialsys.com as gisent1-owner.sde"
gdb_bound= r'M:\AARP\DevelopmentEnvironment\database-connections\aarpsql.aarpdev.spatialsys.com as gisent1-owner.sde\gisent1.DBO.US_Boundaries'

#remote computer locations
#gdb = r"E:\sde-db-connections"
#gdb = r"E:"
#slash = "\\"
#con = "sde-db-connections"
#sde = "aarpsql.aarpdev.spatialsys.com as gisent1-owner.sde"
#gdb_bound = r"E:\sde-db-connections\aarpsql.aarpdev.spatialsys.com as gisent1-owner.sde\gisent1.DBO.US_Boundaries" 

#adm table location
#adm_table = os.path.join(gdb, "gisent1.DBO.admGPServiceSettings")

adm_table = os.path.join(gdb, sde, "gisent1.DBO.admGPServiceSettings")

#fields in adm table
name_field = "name"
value_field = "value"



try:
    def join_geog_csv(method, geography, geog_field, CSV_Table, CSV_Field_for_Join, Keep_All_Target_Features, Join_Output):

       def TakeOutTrash(dataset):
          #get rid of feature layer if already exists
          if arcpy.Exists(dataset):
             arcpy.AddMessage("Previous layer name: " + layer_name)
             arcpy.management.Delete(dataset)
       
       #here
       arcpy.AddMessage("\nYou selected " + geography + " as your geography.\n")

       arcpy.AddMessage(adm_table)
       adm_table_view = "gisent1.DBO.admGPServiceSettings"

       #TakeOutTrash(adm_table_view) #delete table if already exists
       #arcpy.MakeTableView_management(adm_table, adm_table_view) #have to make table so gp service sees it as a table?
       #arcpy.MakeQueryTable_management (adm_table, adm_table_view, "USE_KEY_FIELDS")
       desc = arcpy.Describe(adm_table)

       for field in desc.fields:
           arcpy.AddMessage(field.name)

           #query for geography selected
           query = "duj_gdb_" + ''.join(geography.split()).lower()   #remove spaces and convert to lowercase
           
           #access table  #pass it a query to get one row
           cursor = arcpy.SearchCursor(adm_table, where_clause="name = '" + query + "'")

           #go through each row
           for row in cursor:
               #if row.getValue(name_field) == query: #find row in name field that equals query
               Input_Layer = os.path.join(gdb_bound,row.getValue(value_field)) #value of value field for query /if row equals equery, get the corresponding value of the value field and set that equal to input_layer

           #delete cursor, row objects
           del cursor, row
           
       #Input layer selected
       layer_name = Input_Layer.split('\\',6)[-1]
       arcpy.AddMessage("\nThe input layer that will be used is " + layer_name + ".\n")

       #need to get fields from layer
       #just manually create field list in drop down in validation depending on what layer picked
       arcpy.AddMessage("\nThe " + geog_field + " field will be used for the geography join.\n")


       #csv input
       arcpy.AddMessage("\nThe CSV table that will be used is " + CSV_Table + ".\n")

       #keep all features
       if Keep_All_Target_Features == '#' or not Keep_All_Target_Features:
           Keep_All_Target_Features = "false" # provide a default value if unspecified

       #make feature layer
       #feature_layer = layer_name  #needs to be automatically created
       arcpy.AddMessage(Input_Layer)
       #arcpy.AddMessage("Previous layer name: " + layer_name)
       
       TakeOutTrash(layer_name) #delete feature layer if already exists
       
       arcpy.MakeFeatureLayer_management(Input_Layer, layer_name)
       #arcpy.AddMessage('\nfeature layer made')

       #csv join field
       arcpy.AddMessage("\nThe CSV field that will be used for the join is " + CSV_Field_for_Join + ".\n")

       # Process: Add Join
       arcpy.AddJoin_management(layer_name, geog_field, CSV_Table, CSV_Field_for_Join, Keep_All_Target_Features)
       arcpy.AddMessage('\nGeography and csv table join done.\n')

       #output parameter
       arcpy.SetParameter(5, layer_name)    #adds a new output in mxd; feature layer still being removed though...
       arcpy.AddMessage('\nOut put layer ' + Join_Output)

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
