# ArcGIS
Python modules using ArcPy and arcgis to access Geodatabases

This project is for modules that utilize ArcGIS packages to interact with databases. 

CONTENTS:
reporter.py - a simple script that exports data from a database (tested with gdb and sde) to a csv file. contains some minor cvs formatting.

        Geodatabase Reporter

        SUMMARY:
        This Module extracts all information from an ArcGIS geodatabase into a csv file.
        The ArcPy package is required to run this module. ArcPy is provided in ArcGIS Pro.
        Written for Python3 and must be run in the arcgispro-py3 environment provided with ArcGIS Pro.

        Feel free to contact me with any questions at torrance.m.graham@gmail.com


        OPTIONS:
        To remove table contents for faster execution and less details, comment out the two line statements:  
          "display_table_contents(table, cw)"


        QA:
          Q: Excel wont completely load the output file?
          A: Excel limits a file to only show 1,000,000 rows. A workaround for this is 
                   to import the csv file to a power query. To do this follow the guide linked below.
            https://blogs.technet.microsoft.com/josebda/2017/02/12/loading-csvtext-files-with-more-than-a-million-rows-into-excel/


