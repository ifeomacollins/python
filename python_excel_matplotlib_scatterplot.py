#Author: Ifeoma Collins, GIS Research Analyst
#Date: May 4, 2017
#Read .xls or csv file and plot scatterplot with 2 columns using matplotlib and log scale on x-axis

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import csv
import xlrd


x = []
y = []

'''
#csv file option
with open(r'file_here.csv', 'r') as csvfile:
	plots = csv.reader(csvfile, delimiter=',')
	csvfile.readline() #skip first line
	for row in plots:
		x.append((row[6]))
		y.append((row[3]))
'''

#xls sheet option
workbook = xlrd.open_workbook(r'file_here.xls')
worksheet = workbook.sheet_by_index(0)

sheets = workbook.sheets()

#x
for row in range(1, sheets[0].nrows):
    xrow = sheets[0].cell_value(row, 10)
    x.append(xrow)

#y
for row in range(1, sheets[0].nrows):
    yrow = sheets[0].cell_value(row,7)
    y.append(yrow)

print x

print y

# Draw the grid lines
plt.grid(True)

#plt.plot(x,y,label='Alert Density')
plt.xlabel('LN Annual Average % Difference')
plt.ylabel('Density of # of Current Alerts by Area (ha)')

#plt.legend()
plt.title('2015 Annual Average Alert Intensity 2016 Week 30')

##log
#scatter plot x, y #place before the log scale is set
plt.scatter(x,y)

# 'symlog' scaling, however, handles negative values nicely
plt.xscale('symlog') #turn on for x log scale

plt.show()

