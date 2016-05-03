# Name: download_census_files.py
# Description:  download and unzip census files for each state...PUMA
#author: Ifeoma Collins
#Date: May 3, 2016


#for extracting zip files
import zipfile, StringIO


#Call urllib2 library to integrate Python with web services
import urllib2
from urllib2 import urlopen

print "Going to Census url with list of zipped files"

#small num loop
for num in range(1, 10): #number range for links
    #need to do if URL exists...
    url = "http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_0" + str(num) + "_puma10_500k.zip"
    #print url
    
    try:
        #if url exists
        print "small number links"
        print url
        f = urllib2.urlopen(url)
        deadLinkFound = False
        #print f
        data = f.read()
        #print data
        with open(r'C:\Users\icollins\Downloads\puma\cb_2015_0' + str(num) + '_puma10_500k.zip', "wb") as code:
            code.write(data)

        print "unzipping files to folder - small num"
        zipDocument = zipfile.ZipFile(StringIO.StringIO(data))

        #save extracted files here
        zipDocument.extractall(r'C:\Users\icollins\Downloads\puma\extracted')

    except:
        #if url doesn't exist ignore
        deadLinkFound = True

#big num loop
for num in range (10,57):
    url = "http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_" + str(num) + "_puma10_500k.zip"

    try:
        #if url exists
        print "big number links"
        print url
        f = urllib2.urlopen(url)
        deadLinkFound = False
        #print f
        data = f.read()
        #print data
        with open(r'C:\Users\icollins\Downloads\puma\cb_2015_' + str(num) + '_puma10_500k.zip', "wb") as code:
            code.write(data)

        print "unzipping files to folder - big num"
        zipDocument = zipfile.ZipFile(StringIO.StringIO(data))

        #save extracted files here
        zipDocument.extractall(r'C:\Users\icollins\Downloads\puma\extracted')

    except:
        #if url doesn't exist ignore
        deadLinkFound = True



print "All PUMA 2015 Census files from each state downloaded and extracted"
print "Finished"
