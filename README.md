# ArcGIS-MapBook-Toolbox
Map scripting can be integrated with Data Driven Pages to create a map book that includes custom maps on different pages while using a single map document. In order to use Data Driven Pages to build a map book you need to use Arcpy.mapping. This module provides functions to automate exporting and printing. Arcpy.mapping was designed primarily to manipulate the contents of existing map documents (.mxd) and layer files (.lyr). It also provides functions to automate exporting and printing. Arcpy.mapping can be used to automate map production; it extends the capabilities of Data Driven Pages and is required to build complete map books because it includes functions to export to, create, and manage PDF documents. Finally, arcpy.mapping scripts can be published as geoprocessing services and the script functionality can be made available to web applications. 
The current scripting Toolbox, MapBook, enables to include dynamic data frame title, continuous page number for all of the target layers, setting the print properties and appending the generated PDF files from the title page and target data layers with the aid od Data Driven Pages and Arcpy.mapping. 
