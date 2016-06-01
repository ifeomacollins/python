# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# join_service.py
# edited by Ifeoma Collins May 25 2016
# Usage: join <Input_Layer> <Input_Join_Field> <CSV_Table> <CSV_Field_for_Join> <Keep_All_Target_Features> <Join_Output> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, traceback, os

# Script parameters
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

#geography variables
county = 'County'
state = 'State'
zcta = 'ZCTA'
blockgroup = 'Block Group'
condist = 'Congressional District'
puma = 'PUMA'

gdb = r"E:\db\US_Boundaries" 
county20_fc = os.path.join(gdb, "gis.DBO.County_20m")
state20_fc =  os.path.join(gdb, "gis.DBO.State_20m")
zcta_fc = os.path.join(gdb, "gis.DBO.ZCTA_500k")
blockgroup_fc = os.path.join(gdb, "gis.DBO.BlockGroup_Detailed")
condist_fc = os.path.join(gdb, "gis.DBO.ConDist_20m")
puma_fc = os.path.join(gdb, "gis.DBO.Puma_500k")


arcpy.AddMessage(gdb)
arcpy.AddMessage(state20_fc)

def TakeOutTrash(dataset):  #get rid of feature layer if already exists
   if arcpy.Exists(dataset):
       arcpy.management.Delete(dataset)


try:
    arcpy.AddMessage("\nYou selected " + geography + " as your geography.\n")
    
    #geography selection
    if geography == county:
        Input_Layer = county20_fc
        
    if geography == state :
        Input_Layer = state20_fc 

    if geography == zcta:
        Input_Layer = zcta_fc

    if geography == blockgroup:
        Input_Layer = blockgroup_fc

    if geography == condist:
        Input_Layer = condist_fc

    if geography == puma:
        Input_Layer = puma_fc

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
    arcpy.AddMessage("Previous layer name: " + layer_name)
    
    TakeOutTrash(layer_name) #delete feature layer if already exists
    
    tmp_layer = arcpy.MakeFeatureLayer_management(Input_Layer, layer_name)
    #arcpy.AddMessage('\nfeature layer made')

    #csv join field
    arcpy.AddMessage("\nThe CSV field that will be used is for the join is " + CSV_Field_for_Join + ".\n")

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

