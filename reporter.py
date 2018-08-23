#!/usr/bin/env python

__author__ = "Torrance Graham"
__email__ = "torrance.m.graham@gmail.com"
__version__ = "0.2"
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
import os
from pathlib import Path

#-------------------------------------------
# Set DataBase and Output File - Change these locations to desired database and output path.
env.overwriteOutput = True
env.workspace = r"C:\GIS\Database"
outputFile = r'C:\GIS\output.csv'


# write_to_csv Helper Functions --------------
def display_datasets(datasets, cw):
    r""" display_datasets traverses through each dataset in a list of datasets
    Helper Functions: display_feature_classes()
    Parameters: datasets (geodatabase list of datasets given by arcpy.ListDatasets), cw (the csv.writer object)
    """
    
    cw.writerow(["DATASETS"])
    for dataset in datasets:
        cw.writerow([dataset])

        cw.writerow(["FULL PATH", "FEATURE CLASS"])

        featureClasses = arcpy.ListFeatureClasses("*", "", dataset)
        path = os.path.join(env.workspace, dataset)
        display_feature_classes(featureClasses, cw, path)
        cw.writerow("")
        
def display_feature_classes(featureClasses, cw, path= env.workspace):
    r""" display_feature_classes traverses through each featureClass in a list of featureClasses
    Helper Functions: display_table_contents()
    Parameters: featureClasses (geodatabase list of featureClasses given by arcpy.ListFeatureClasses), cw (the csv.writer object),
                path (optional parameter that specifies the full path of a featureClass, Default: the main path of the database) 
    """
        
    for featureClass in featureClasses:
        
        display_path = os.path.join(path, featureClass)
        display_path = Path(display_path)
        display_path = display_path.parts[-2:]
        display_path = Path(*display_path[-2:])
        
        cw.writerow([display_path, featureClass])

        # Comment this line out if you dont want to display the table contents
        display_table_contents(featureClass, cw, path)
            
def display_tables(tables, cw):
    r""" display_tables traverses through each table in a list of tables
    Helper Functions: display_table_contents()
    Parameters: tables (geodatabase list of tables given by arcpy.ListTables), cw (the csv.writer object)
    """
    
    cw.writerow(["FUll PATH", "TABLES"])
    for table in tables:

        display_path = os.path.join(env.workspace, table)
        display_path = Path(display_path)
        display_path = display_path.parts[-2:]
        display_path = Path(*display_path[-2:])
        
        cw.writerow([display_path, table])

        # Comment this line out if you dont want to display the table contents
        display_table_contents(table, cw)

def display_table_contents(arcClass, cw, path= env.workspace):
    r""" display_table_contents displays the values for each field in a datatype.
    Parameters: arcClass (The arcpy datatype to cursor through), cw (the csv.writer object), path (optional parameter that specifies the full path of arcClass, Default: the main path of the database) 
    """
    full_path = os.path.join(path, arcClass)
    
    display_path = Path(full_path)
    display_path = display_path.parts[-2:]
    display_path = Path(*display_path[-2:])
    
    # Displays Field Names
    field_Names = [field.name for field in arcpy.ListFields(full_path)]
    field_Names_Header = ["FULL PATH"]
    field_Names_Header.extend(field_Names)
    cw.writerow(field_Names_Header)
    
    # Display Table values
    try:
        cursor = arcpy.da.SearchCursor(full_path, field_Names)

    except TypeError:
        #testing area for tomorrow
        print("field names for " + arcClass + ": ")
        for x in range(len(field_Names)):
            print(field_Names[x])

        newField_Names = map(str, field_Names)
        cursor = arcpy.da.SearchCursor(full_path, newField_Names)

    for row in cursor:
        
        updated_row = [display_path]
        # Removes return commands from values in row
        for index in row:
            if type(index) == str:
                index = index.replace('\r', '')
                index = index.replace('\n', '')
                updated_row.append(index)
            else:
                updated_row.append(index)
                
        cw.writerow(updated_row)
#-----------------------------------------------



# Main Functions -------------------------------
def write_to_csv(outputFile):
    r""" write_to_csv uses arcpy.List<datatype> to collect and print the contents of a gdb to an csv file.
    Helper Functions: display_datasets(), display_feature_classes(), display_tables()
    Parameters: outputFile(a designated csv file to print the data to.)
    """

    tables = arcpy.ListTables("*")
    datasets = arcpy.ListDatasets("*")
    featureClasses = arcpy.ListFeatureClasses("*")

    # encoding='utf-8' required for databases containing special characters in Python 3.5.4
    with open(outputFile, 'w', encoding='utf-8') as file:
        
        cw = csv.writer(file, delimiter= ',', quotechar = '"', lineterminator='\n', quoting = csv.QUOTE_MINIMAL)

        # Displays database
        cw.writerow(["DATABASE"])
        cw.writerow([env.workspace])
        
        cw.writerow("")

        display_datasets(datasets, cw)

        cw.writerow("")
        cw.writerow(["FEATURE CLASSES THAT ARENT IN A DATASET"])
        display_feature_classes(featureClasses, cw)
   
        cw.writerow("")
        
        display_tables(tables, cw)
            

#---------------------------------------------
if __name__ == '__main__':
    write_to_csv(outputFile)
