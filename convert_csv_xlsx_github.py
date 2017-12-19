#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:  convert csv files in folder to xlsx and save to another folder
#
# Author:      Ifeoma.Collins
#
# Created:     19-12-2017
# Copyright:   (c) Ifeoma.Collins 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


#https://stackoverflow.com/questions/12976378/openpyxl-convert-csv-to-excel
#https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python


import csv, openpyxl, os, glob


#list of csv files in directory
csv_folder = r"C:\csvs" + "\\"

#save xls in this folder
xlxs_folder =  r"C:\xlsx" + "\\"
os.chdir(csv_folder)

wb = openpyxl.Workbook()
ws = wb.active

for file in glob.glob("*.csv"):
    filename = csv_folder+file
    print filename
    f = open(filename)
    reader = csv.reader(f,delimiter=",") #this character matters. use , to put each value in a column

    for row in reader:
        ws.append(row)
    f.close()

    wb.save(xlxs_folder+file[:-4]+".xlsx")


print "done"
