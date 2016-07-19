# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# join_query_function.py
# edited by Ifeoma Collins May 25 2016
# Usage: join <Input_Layer> <Input_Join_Field> <CSV_Table> <CSV_Field_for_Join> <Keep_All_Target_Features> <Join_Output> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, traceback, os, csv

# Script parameters

#gdb location
#local computer
#gdb = r"M:\AARP\DevelopmentEnvironment\database-connections\gisent2 as gisent1-owner.sde"
#gdb_bound = r"M:\AARP\DevelopmentEnvironment\database-connections\gisent2 as gisent1-owner.sde\gisent2.DBO.US_Boundaries"
#gdb =r"M:\AARP\DevelopmentEnvironment\database-connections"
#sde = "gisent2 as gisent1-owner.sde"
#gdb_bound= r'M:\AARP\DevelopmentEnvironment\database-connections\gisent2 as gisent1-owner.sde\gisent2.DBO.US_Boundaries'

#remote computer locations
#gdb = r"E:\sde-db-connections"
#gdb = r"E:"
#slash = "\\"
#con = "sde-db-connections"
#sde = "gisent2 as gisent1-owner.sde"
gdb_bound = r"E:\sde-db-connections\gisent2 as gisent1-owner.sde\gisent2.DBO.US_Boundaries" 

#adm table location
#adm_table = os.path.join(gdb, "gisent2.DBO.admGPServiceSettings")
adm_table = r"E:\sde-db-connections\gisent2 as gisent1-owner.sde\gisent2.DBO.admGPServiceSettings"

#empty geocoding layer when join method is selected
geocoded_results_empty = r"E:\sde-db-connections\gisent2 as gisent1-owner.sde\gisent2.DBO.Geocoded_Results_Empty"

#empty join layer when geocoding method is selected
joinoutput_results_empty = r"E:\sde-db-connections\gisent2 as gisent1-owner.sde\gisent2.DBO.Join_Output_Empty"

#shapefile to store geocoded_results
geocoded_results = r"E:\sde-db-connections\gisent2 as gisent1-owner.sde\gisent2.DBO.Geocoded_Results"

#fields in adm table
name_field = "name"
value_field = "value"

#geocode_result = "C:\\Users\\icollins\\Documents\\ArcGIS\\Default.gdb\\Sacramento_singleline_Geocod_2"
#save to scratch space than designated spot on disk so when multiple gp services run won't lock
#local computer locaation: C:\Users\%user%\AppData\Local\Temp\scratch.gdb.
#gp service location: c:\arcgisserver\directories\arcgisjobs\%service%_gpserver\%jobid%\scratch\scratch.gdb.
geocode_result = arcpy.env.scratchGDB + "\\" + "geocoding_results"   #added geocoding_results so will add display

csv_result = arcpy.env.scratchGDB + "\\" + "csv_results.csv" 


try:
    def join_geog_csv(method, geography, geog_field, CSV_Table, CSV_Field_for_Join, Keep_All_Target_Features, Join_Output, Geocoded_Locations, Unmatched_Rows):

       if method == 'Join to Map Features':
          #here
           arcpy.AddMessage("\nYou selected " + method + " as your method.\n")

           def TakeOutTrash(dataset):
              #get rid of feature layer if already exists
              if arcpy.Exists(dataset):
                 arcpy.AddMessage("Previous layer name: " + layer_name)
                 arcpy.management.Delete(dataset)
           
           #here
           arcpy.AddMessage("\nYou selected " + geography + " as your geography.\n")

           arcpy.AddMessage(adm_table)
           adm_table_view = "gisent2.DBO.admGPServiceSettings"

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
                   Input_Layer = os.path.join(gdb_bound,row.getValue(value_field)) + "_1" #value of value field for query /if row equals equery, get the corresponding value of the value field and set that equal to input_layer

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
           arcpy.SetParameter(6, layer_name)    #adds a new output in mxd; feature layer still being removed though...
           arcpy.AddMessage('\nOut put layer ' + Join_Output)

           #Empty Geocoded results for feature layer requirement
           arcpy.SetParameter(7, geocoded_results_empty)
           
       if method == 'Geocoded Addresses':
           #Overwrite the output feature class if it already exists
           arcpy.env.overwriteOutput = True

           #Delete feature class if it exists
           #if arcpy.Exists(fc):
               #arcpy.Delete_management(fc)

           arcpy.AddMessage("\nYou selected " + method + " as your method.\n")
           
           address_table = CSV_Table

           #for US Composite
           #address_locator = r"Z:\Locators\USA"
           #address_fields = "Address Address VISIBLE NONE;City <None> VISIBLE NONE;Region <None> VISIBLE NONE;Postal <None> VISIBLE NONE"

           #for point address locator
           address_locator = r"Z:\Locators\USA_PointAddress"
           address_fields = "Street " + CSV_Field_for_Join + " VISIBLE NONE;City <None> VISIBLE NONE;State <None> VISIBLE NONE;ZIP <None> VISIBLE NONE"

           arcpy.AddMessage("\nThe CSV table that will be used is " + address_table + ".\n")
           arcpy.AddMessage("\nThe field mapping input is " + address_fields + ".\n")
           arcpy.AddMessage("\nThe locator is " + address_locator + ".\n")
           arcpy.AddMessage("\nResults will be stored here " + geocode_result + ".\n")

           #featurelayer code
           Input_Layer = geocode_result

           arcpy.AddMessage(Input_Layer)
           
           #TakeOutTrash(Input_Layer) #delete feature layer if already exists
           
           arcpy.GeocodeAddresses_geocoding(address_table, address_locator, address_fields, Input_Layer)

           arcpy.AddMessage('Geocoding done.\n')

           arcpy.SetParameter(7, Input_Layer) 

           #unmatched addresses

           #get list of fields from uploaded csv
           desc = arcpy.Describe(address_table)

           # Use ListFields to get a list of field objects
           fieldObjList = arcpy.ListFields(address_table)
           fieldnames = [f.name for f in fieldObjList]
           arcpy.AddMessage("Field names in uploaded csv are \n ")
           arcpy.AddMessage(fieldnames)

           #select rows with status equal u
           where_clause = "Status = 'U' "
           geocoded_u_lyr = "unmatched_results"

           arcpy.MakeFeatureLayer_management (Input_Layer, geocoded_u_lyr)

           arcpy.AddMessage("Make feature layer done.\n")
           
           arcpy.SelectLayerByAttribute_management (geocoded_u_lyr, "NEW_SELECTION", where_clause)

           urows_num = arcpy.GetCount_management(geocoded_u_lyr)

           arcpy.AddMessage("Number of umatched rows in results is " + str(urows_num) + ".\n")

           #only add fields from uploaded csv in unmatched rows csv

           #store row values to corresponding fields in unmatched csv

           #export this data to unmatched_rows csv
           with open(csv_result, 'wb') as f:
               w = csv.writer(f)
               w.writerow(fieldnames)
               for row in arcpy.SearchCursor(geocoded_u_lyr):
                   field_vals = [row.getValue(field.name) for field in fieldObjList]
                   w.writerow(field_vals)
               del row

           arcpy.SetParameter(8, csv_result) 
           
           arcpy.AddMessage('\nGeocoding and unmatched addresses listed in table done.\n')

           #Empty Joinoutput results for feature layer requirement
           arcpy.SetParameter(6, joinoutput_results_empty)
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
