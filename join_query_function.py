# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# join_query_function.py
# created/edited by Ifeoma Collins May 25 2016
# Updated: July 21, 2016
# Description: Join the Geography polygon by querying table to uploaded CSV based on join fields and output to map or
#Geocode addresses based on csv uploaded
#modular for easier updates and also to delete default values
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, traceback, os, csv

# Script parameters

#local computer
#gdb_bound = r"M:\AARP\DevelopmentEnvironment\database-connections\gisent2 as gisent1-owner.sde\gisent2.DBO.US_Boundaries"

#remote computer locations
gdb_bound = r"E:\sde-db-connections\gisent2 as gisent1-owner.sde\gisent2.DBO.US_Boundaries" 

#adm table location
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

#save to scratch space than designated spot on disk so when multiple gp services run won't lock
#local computer locaation: C:\Users\%user%\AppData\Local\Temp\scratch.gdb.
#gp service location from web map: c:\arcgisserver\directories\arcgisjobs\%service%_gpserver\%jobid%\scratch\scratch.gdb.
geocode_result = arcpy.env.scratchGDB + "\\" + "geocoding_results"   #added geocoding_results so will add display

#csv_empty = arcpy.env.scratchGDB + "\\" + "csv_results_empty.csv" 
csv_empty = r"E:\sde-db-connections\gisent2 as gisent1-owner.sde\gisent2.DBO.unmatched_empty"

try:
    def join_geog_csv(method, geography, geog_field, CSV_Table, CSV_Field_for_Join, Keep_All_Target_Features, Join_Output, Geocoded_Locations, Unmatched_Rows):

       if method == 'Join to Map Features':
           arcpy.AddMessage("\nYou selected " + method + " as your method.\n")

           def TakeOutTrash(dataset):
              #get rid of feature layer if already exists
              if arcpy.Exists(dataset):
                 arcpy.AddMessage("Previous layer name: " + layer_name)
                 arcpy.management.Delete(dataset)
           
           #here
           arcpy.AddMessage("\nYou selected " + geography + " as your geography.\n")

           adm_table_view = "gisent2.DBO.admGPServiceSettings"

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
           arcpy.AddMessage("\nThe " + geog_field + " field will be used for the geography join.\n")

           #csv input
           arcpy.AddMessage("\nThe CSV table that will be used is " + CSV_Table + ".\n")

           #keep all features
           if Keep_All_Target_Features == '#' or not Keep_All_Target_Features:
               Keep_All_Target_Features = "false" # provide a default value if unspecified

           #make feature layer
           #feature_layer = layer_name  #needs to be automatically created
           
           TakeOutTrash(layer_name) #delete feature layer if already exists
           
           arcpy.MakeFeatureLayer_management(Input_Layer, layer_name)

           #csv join field
           arcpy.AddMessage("\nThe CSV field that will be used for the join is " + CSV_Field_for_Join + ".\n")

           # Process: Add Join
           arcpy.AddJoin_management(layer_name, geog_field, CSV_Table, CSV_Field_for_Join, Keep_All_Target_Features)
           arcpy.AddMessage('\nGeography and csv table join done.\n')

           #output parameter
           arcpy.SetParameter(6, layer_name)    #adds a new output in mxd
           arcpy.AddMessage('\nOut put layer ' + Join_Output)

           #Empty Geocoded results for feature layer requirement
           arcpy.SetParameter(7, geocoded_results_empty)

           #emtpy csv for web map
           arcpy.SetParameter(8, csv_empty)
           
       if method == 'Geocoded Addresses':
           #store results of unmatched addresses here
           csv_result = arcpy.env.scratchGDB + "\\" + "csv_results.csv"
           
           #Overwrite the output feature class if it already exists
           arcpy.env.overwriteOutput = True

           arcpy.AddMessage("\nYou selected " + method + " as your method.\n")
           
           address_table = CSV_Table

           #for point address locator
           edrive = r"\\aarpgis.aarpdev.spatialsys.com\e\Locators"
           address_locator = os.path.join(edrive, "USA_PointAddress")
           
           address_fields = "Street " + CSV_Field_for_Join + " VISIBLE NONE;City <None> VISIBLE NONE;State <None> VISIBLE NONE;ZIP <None> VISIBLE NONE"

           arcpy.AddMessage("\nThe CSV table that will be used is " + address_table + ".\n")
           arcpy.AddMessage("\nThe field mapping input is " + address_fields + ".\n")
           arcpy.AddMessage("\nThe locator is " + address_locator + ".\n")
           arcpy.AddMessage("\nResults will be stored here " + geocode_result + ".\n")

           #featurelayer code
           Input_Layer = geocode_result
           
           arcpy.GeocodeAddresses_geocoding(address_table, address_locator, address_fields, Input_Layer)

           arcpy.AddMessage('Geocoding done.\n')

           #unmatched addresses

           #get list of fields from uploaded csv
           desc = arcpy.Describe(address_table)

           # Use ListFields to get a list of field objects
           fieldObjList = arcpy.ListFields(address_table)
           fieldnames = [f.name for f in fieldObjList]
           #arcpy.AddMessage("Field names in uploaded csv are \n ")
           #arcpy.AddMessage(fieldnames)

           #select rows with status equal u
           where_clause = "Status = 'U' "
           geocoded_u_lyr = "unmatched_results"

           arcpy.MakeFeatureLayer_management (Input_Layer, geocoded_u_lyr)

           arcpy.AddMessage("Make feature layer done for unmatched.\n")
           
           arcpy.SelectLayerByAttribute_management (geocoded_u_lyr, "NEW_SELECTION", where_clause)

           urows_num = arcpy.GetCount_management(geocoded_u_lyr)

           #arcpy.AddMessage("Number of umatched rows in results is " + str(urows_num) + ".\n")

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

           #unselect features
           arcpy.SelectLayerByAttribute_management (geocoded_u_lyr, "CLEAR_SELECTION")

           #make new feature layer with new name for geocding results
           arcpy.MakeFeatureLayer_management (Input_Layer, "geocoding_results")

           arcpy.AddMessage("Make feature layer done for matched.\n")

           #do query status = M // so web map extent won't be NAN
           where_clause = "Status = 'M' "
           arcpy.SelectLayerByAttribute_management ("geocoding_results", "NEW_SELECTION", where_clause)

           mrows_num = arcpy.GetCount_management("geocoding_results")

           #arcpy.AddMessage("Number of matched rows in results is " + str(mrows_num) + ".\n")

           outFeatureClass = arcpy.env.scratchGDB + "\\" + "geocoding_results_matches" 

           #copy selection to another feature class
           arcpy.CopyFeatures_management("geocoding_results", outFeatureClass)

           #set parameter 7 geocoder results with Match here

           arcpy.SetParameter(7, outFeatureClass) 
           
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