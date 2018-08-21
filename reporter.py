#!/usr/bin/env python

__author__ = "Torrance Graham"
__email__ = "torrance.m.graham@gmail.com"
__version__ = "0.1"
__status__ ="Production"

'''
This Module extracts all information from an ArcGIS geodatabase into a csv file.
The ArcPy package is required to run this module. ArcPy is provided in ArcGIS Pro.
Written for Python3 and must be run in the arcgispro-py3 environment provided with ArcGIS Pro.

Feel free to contact me with any questions at torrance.m.graham@gmail.com
'''


import arcpy
from arcpy import env
import csv


#-------------------------------------------
# Set DataBase and Output File - Change these locations to desired database and output path.
env.overwriteOutput = True
env.workspace = r'C:\GIS\geodatabase.gdb'
outputFile = r'C:\GIS\output.csv'


#---------------------------------------------
def write_to_csv(outputFile):
    # Geodatabase extraction
    tables = arcpy.ListTables("*")
    datasets = arcpy.ListDatasets("*")
    featureClasses = arcpy.ListFeatureClasses("*")
    
    with open(outputFile, 'w') as file:

        cw = csv.writer(file, delimiter= ',', quotechar = '"', lineterminator='\n', quoting = csv.QUOTE_MINIMAL)
        
        # Creates DictWriter object to create headers for each feature class
        fcHeader = csv.DictWriter(file, lineterminator='\n', fieldnames = ["FEATURE CLASS", "DATA COUNT"])
        
        # Displays database
        cw.writerow(["DATABASE"])
        cw.writerow([env.workspace])
        cw.writerow("")

        # Displays Datasets
        cw.writerow(["DATASETS"])
        for dataset in datasets:
            cw.writerow([dataset])

            fcHeader.writeheader()

            # Displays the features classes of each dataset and data count
            for featureClass in arcpy.ListFeatureClasses("*", "", dataset):
                count = arcpy.GetCount_management(featureClass).getOutput(0)
                cw.writerow([featureClass, count])

                # Displays Field Names
                field_Names = [field.name for field in arcpy.ListFields(featureClass)]
                cw.writerow(field_Names)

                # Display Table values
                cursor = arcpy.da.SearchCursor(featureClass, field_Names)
                for row in cursor:
                    cw.writerow(row)

            cw.writerow("")


        # Displays Feature Classes in main database
        cw.writerow(["FEATURE CLASSES"])
        for featureClass in featureClasses:
            count = arcpy.GetCount_management(featureClass).getOutput(0)
            cw.writerow([featureClass, count])
            # Displays Field Names
            field_Names = [field.name for field in arcpy.ListFields(featureClass)]
            cw.writerow(field_Names)

            # Display Table values
            cursor = arcpy.da.SearchCursor(featureClass, field_Names)
            for row in cursor:
                cw.writerow(row)
                
        cw.writerow("")

        # Displays Tables
        cw.writerow(["TABLES"])
        for table in tables:
            count = arcpy.GetCount_management(table).getOutput(0)
            cw.writerow([table, count])
            
            # Displays Field Names
            field_Names = [field.name for field in arcpy.ListFields(table)]
            cw.writerow(field_Names)

            # Display Table values
            cursor = arcpy.da.SearchCursor(table, field_Names)
            for row in cursor:
                cw.writerow(row)
        
        cw.writerow("")
            

#---------------------------------------------
if __name__ == '__main__':
    
    write_to_csv(outputFile)
