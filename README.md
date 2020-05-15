# ArcGIS-MapBook-Toolbox

MapBook.tbx contains two script files to automate ArcGIS maps production:<br />
PDFformay.py<br />
PNGformat.py

The current scripting Toolbox, MapBook, enables to include dynamic data frame title, continuous page number for all of the target layers, setting the print properties and appending the generated PDF files from the title page and target data layers with the aid od Data Driven Pages and Arcpy.mapping.

To use this toolbox, the Data Driven Pages and laout should be defined in mapdocument environment. Data Driven Pages Tutorial is available at [Data Driven Pages](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00sr00000006000000).


![alt text here](https://github.com/Nina-Om/ArcGIS-MapBook-Toolbox/blob/master/toolbox.PNG)

![alt text here](https://github.com/Nina-Om/ArcGIS-MapBook-Toolbox/blob/master/pdf.PNG)


![alt text here](https://github.com/Nina-Om/ArcGIS-MapBook-Toolbox/blob/master/png.PNG)


## MapDocument

Map scripting can be integrated with Data Driven Pages to create a map book that includes custom maps on different pages while using a single map document. In order to use Data Driven Pages to build a map book you need to use Arcpy.mapping. This module provides functions to automate exporting and printing. Arcpy.mapping was designed primarily to manipulate the contents of existing map documents (.mxd) and layer files (.lyr). It also provides functions to automate exporting and printing. Arcpy.mapping can be used to automate map production; it extends the capabilities of Data Driven Pages and is required to build complete map books because it includes functions to export to, create, and manage PDF documents.

## Links for more information
[Data Driven Pages](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00sr00000006000000)<br />
[Arcpy.mapping](https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/introduction-to-arcpy-mapping.htm)<br />
[Relevant blog post](https://www.esri.com/arcgis-blog/products/arcgis-desktop/mapping/combining-data-driven-pages-with-python-and-arcpy-mapping/)<br />
[MapDocument](https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/mapdocument-class.htm)

## Toolbox Parameters list
1. PDFformat.py<br />
Layer : Input feature layer <br />
out_ws : a workspace for storing the generated files<br /> 
tmpPdf : mapbook PDf file name 
2. PNGformat.py<br />
Layername : Input feature layer<br />
out_ws : a workspace for storing the generated files <br />
resolution  : image resolution

## Python Scripts
### 1. PNGformat.py

```python
import arcpy, os, string

# Read the parameter values:
Layername = arcpy. GetParameter(0)
out_ws = arcpy.GetParameterAsText(1)
resolution = arcpy.GetParameterAsText(2)
#
mxd = arcpy.mapping.MapDocument("CURRENT")
df = mxd.activeDataFrame
ddp = mxd.dataDrivenPages
# 
Layers = arcpy.mapping.ListLayers(Layername, "", df)
```
Assign a layer name `Layers[0].name` to dataframe title. Define dataframe `df` Title Element name as `TitleText` in your mapdocument.
```python
TextElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","TitleText")[0]
TextElement.text = Layers[0].name
```
Generate PNG files of the `ddp` pages.
```python
for pageNum in range(1, ddp.pageCount + 1):
  ddp.currentPageID = pageNum
  print "Exporting page {0} of {1}".format(str(ddp.currentPageID), str(ddp.pageCount))
  arcpy.mapping.ExportToPNG(mxd, os.path.join(out_ws, Layers[0].name + str(pageNum) + ".png"), resolution=resolution)
del mxd
```

### 2. PDFformat.py

```python
import arcpy, os, string

# Read the parameter values:
Layername = arcpy. GetParameter(0)
out_ws = arcpy.GetParameterAsText(1)
tmpPdf = arcpy.GetParameterAsText(2)
#
mxd = arcpy.mapping.MapDocument("CURRENT")
df = mxd.activeDataFrame
ddp = mxd.dataDrivenPages
#
Layers = arcpy.mapping.ListLayers(Layername, "", df)
```
Assign a layer name `Layers[0].name` to dataframe title. Define dataframe `df` Title Element name as `TitleText` in your mapdocument.
```python
TextElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","TitleText")[0]
TextElement.text = Layers[0].name
```
Export all `ddp` pages to pdf file `tmpPDF`.
```python
ddp.exportToPDF(os.path.join(out_ws , tmpPdf + ".pdf"), "ALL")
#tmpPdf.appendPages(os.path.join(out_ws , tmpPdf + ".pdf"))
del mxd
tmpPdf.updateDocProperties(pdf_open_view="USE_THUMBS",
pdf_layout="SINGLE_PAGE")
del tmpPdf
```
