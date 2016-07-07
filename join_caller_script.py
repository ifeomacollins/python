# join_caller_script.py
# Created by Ifeoma Collins June 3, 2016
# Usage: join <Input_Layer> <Input_Join_Field> <CSV_Table> <CSV_Field_for_Join> <Keep_All_Target_Features> <Join_Output> 
# Description: Join the Geography polygon by querying table to uploaded CSV based on join fields and output to map
#modular for easier updates and also to delete default values

import arcpy
import sys

import socket #what is this for?
sys.path.append(r'\\' + socket.gethostname() + "M:\icollins\aarp\scripts")

import join_query_function


#parameters in script tool
method = arcpy.GetParameterAsText(0)
geography = arcpy.GetParameterAsText(1)
geog_field = arcpy.GetParameterAsText(2)
CSV_Table = arcpy.GetParameterAsText(3)
CSV_Field_for_Join = arcpy.GetParameterAsText(4)
Keep_All_Target_Features = arcpy.GetParameterAsText(5)
Join_Output = arcpy.GetParameterAsText(6)


#function to call the join query code
def join_query_gp (method, geography, geog_field, CSV_Table, CSV_Field_for_Join, Keep_All_Target_Features, Join_Output):
    if method == '' and geography == '' and geog_field == '' and CSV_Table == '' and CSV_Field_for_Join == '' and Keep_All_Target_Features == '' and Join_Output =='':
        Result = ""
    else:
        Result = join_query_function.join_geog_csv(method, geography, geog_field, CSV_Table, CSV_Field_for_Join, Keep_All_Target_Features, Join_Output)
        arcpy.AddMessage(Result)
    return Result

join_query_gp(method, geography, geog_field, CSV_Table, CSV_Field_for_Join, Keep_All_Target_Features, Join_Output)

'''
#supply values for tool which will become default values to return empty output

if Param1 == '' and Param2 = '':
    Result = ""
else:
    Result = join_query_gp(geography, geog_field, CSV_Table, CSV_Field_for_Join, Keep_All_Target_Features, Join_Output)
'''
