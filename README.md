# ArcGIS-MapBook-Toolbox

MapBook.tbx contains two script files to automate maps production in PNG and PDF format:<br />
PDFformay.py<br />
PNGformat.py

The current scripting Toolbox, MapBook, enables to include dynamic data frame title, continuous page number for all of the target layers, setting the print properties and appending the generated PDF files from the title page and target data layers with the aid od Data Driven Pages and Arcpy.mapping.

# MapDocument

Map scripting can be integrated with Data Driven Pages to create a map book that includes custom maps on different pages while using a single map document. In order to use Data Driven Pages to build a map book you need to use Arcpy.mapping. This module provides functions to automate exporting and printing. Arcpy.mapping was designed primarily to manipulate the contents of existing map documents (.mxd) and layer files (.lyr). It also provides functions to automate exporting and printing. Arcpy.mapping can be used to automate map production; it extends the capabilities of Data Driven Pages and is required to build complete map books because it includes functions to export to, create, and manage PDF documents.



## links for more information
[Data Driven Pages](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00sr00000006000000)<br />
[Arcpy.mapping](https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/introduction-to-arcpy-mapping.htm)<br />
[Relevant blog post](https://www.esri.com/arcgis-blog/products/arcgis-desktop/mapping/combining-data-driven-pages-with-python-and-arcpy-mapping/)<br />
[MapDocument](https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/mapdocument-class.htm)

## Toolbox Parameters list




