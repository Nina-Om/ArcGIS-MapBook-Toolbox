# ArcGIS-MapBook-Toolbox

[Download toolbox here](https://github.com/Nina-Om/ArcGIS-MapBook-Toolbox/blob/master/MapBook.zip)

The current scripting Toolbox, MapBook, loop the data layers and automatically 1. changes the data frame title based on the layer name, 2. adds layers description on the map and 3. generats appended/single PDF files of the selected target layers with the aid of Data Driven Pages and Arcpy.mapping.<br />

MapBook.tbx contains three script files to automate ArcGIS map production:<br />

 1. PDF_MapExport.py  <br />For producing appended PDF files of the selected layers for the selected DD Page Index range, makes change in layout title based on the layer name as well as layer description to the map layout <br />
 2. JPEGbyPageIndex  <br />For producing a JPEG file of the selected layers for one Data Driven Page Number, makes change in layout title based on the layer name <br />
 3. JPEG_by_Layer <br />For producing JPEG files of a selected layer for ALL Data Driven pages, makes change in layout title based on the layer name <br />



To use this toolbox, the Data Driven Pages and layout should be defined in mapdocument environment. Data Driven Pages Tutorial is available at [Data Driven Pages](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00sr00000006000000).


![alt text here](https://github.com/Nina-Om/ArcGIS-MapBook-Toolbox/blob/master/Saved%20Pictures/Toolbox.PNG)

![alt text here](https://github.com/Nina-Om/ArcGIS-MapBook-Toolbox/blob/master/Saved%20Pictures/jpeg.PNG)


## MapDocument

Map scripting can be integrated with Data Driven Pages to create a map book that includes custom maps on different pages while using a single map document. In order to use Data Driven Pages to build a map book you need to use Arcpy.mapping. This module provides functions to automate exporting and printing. Arcpy.mapping was designed primarily to manipulate the contents of existing map documents (.mxd) and layer files (.lyr). Arcpy.mapping can be used to automate map production; it extends the capabilities of Data Driven Pages and is required to build complete map books because it includes functions to export to, create, and manage PDF documents.

## Links for more information
[Data Driven Pages](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00sr00000006000000)<br />
[Arcpy.mapping](https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/introduction-to-arcpy-mapping.htm)<br />
[Relevant blog post](https://www.esri.com/arcgis-blog/products/arcgis-desktop/mapping/combining-data-driven-pages-with-python-and-arcpy-mapping/)<br />
[MapDocument](https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/mapdocument-class.htm)



## Usage
Before using the toolbox:

Please set up Data Driven Pages (DDP), DDP dynamic title, legend, static text or DDP dynamic text to the map layout. 
Uncheck all of the target layers in Table of Contect in Map Document (.mxd) to prevent overlaying the legends.

To add layer description to the map automatically for the selected targer layers in the Table of Content, add static text box. In the layer properties, click on "General" Tab, insert layer description text. For all of the target layers insert appropriate description text (optional).

## Python Scripts
### 1.PDF_MapExport.py

```python
import arcpy, os, string, os.path

# Read the parameter values:
listlayers = arcpy.GetParameter(0)
out_ws = arcpy.GetParameterAsText(1)
pageRangeString = arcpy.GetParameterAsText(2)
multipleFiles = arcpy.GetParameterAsText(3)
res = arcpy.GetParameter(4)

mxd = arcpy.mapping.MapDocument("CURRENT")
df = mxd.activeDataFrame
ddp = mxd.dataDrivenPages

arcpy.AddMessage(listlayers)
arcpy.AddMessage(out_ws)
```
The next lines loop through the selected layers and changes map layout title automatically based on the layer name.
For adding a custom text on the map for each target layer automatically, add a static text box to the map layout and add any text in the layer "Description" in "layer properties" under "General" Tab.
```python
for lyr in listlayers:
  arcpy.AddMessage(lyr)
  lyr = arcpy.mapping.ListLayers(mxd, lyr ,df)[0]
  lyr.visible = True
  arcpy.RefreshActiveView(),arcpy.RefreshTOC()
  TextElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "")
  TextElement[1].text = lyr.name
  TextElement[0].text = lyr.description
```
Loop through all of the desired layers, append selected `ddp` pages to a pdf file `tmpPDF` and export it.
```python
  tmpPdf = os.path.join(out_ws + os.sep + str(lyr.name) + ".pdf")
  ddp.exportToPDF(tmpPdf, "RANGE", pageRangeString, multipleFiles , res)
  lyr.visible = False
  arcpy.RefreshActiveView(),arcpy.RefreshTOC()
  for pageNum in range(1,20):
  if os.path.exists(os.path.join(out_ws + os.sep + "Region" + str(pageNum) + ".pdf")):
   os.remove(os.path.join(out_ws + os.sep + "Region" + str(pageNum) + ".pdf"))
  finalPDF = arcpy.mapping.PDFDocumentCreate(os.path.join(out_ws + os.sep + "Region" + str(pageNum) + ".pdf"))

  for subdir, dirs, files in os.walk(out_ws):
     for file in files:
       if file.endswith("_" + str(pageNum) + ".pdf"):
        finalPDF.appendPages(os.path.join(out_ws + os.sep + file))

     finalPDF.updateDocProperties(pdf_open_view="USE_THUMBS",
     pdf_layout="SINGLE_PAGE")
     finalPDF.saveAndClose()
arcpy.AddMessage("________________________________")
arcpy.AddMessage("***PDF files merged successfulley!***")
del mxd

```

### 2. JPEGbyPageIndex.py
```python
# Read the parameter values:
listlayers = arcpy. GetParameter(0)
out_ws = arcpy.GetParameterAsText(1)
resolution = arcpy.GetParameterAsText(2)
pageNum = arcpy.GetParameter(3)
```
```python
mxd = arcpy.mapping.MapDocument("CURRENT")
df = mxd.activeDataFrame
ddp = mxd.dataDrivenPages
ddp.currentPageID = pageNum
arcpy.RefreshActiveView(),arcpy.RefreshTOC()
arcpy.AddMessage(listlayers)
arcpy.AddMessage(out_ws)
#Layers = arcpy.mapping.ListLayers(Layername, "", df)

for lyr in listlayers:
  arcpy.AddMessage(lyr)
  lyr = arcpy.mapping.ListLayers(mxd, lyr ,df)[0]
  lyr.visible = True
  arcpy.RefreshActiveView(),arcpy.RefreshTOC()
  TextElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TitleText")[0]
  TextElement.text = lyr.name
  arcpy.mapping.ExportToJPEG(mxd, os.path.join(out_ws, lyr.name + str(pageNum) + ".jpeg"), resolution=resolution)
  lyr.visible = False
  arcpy.RefreshActiveView(),arcpy.RefreshTOC()
del mxd
#for pageNum in range(1, ddp.pageCount + 1):
#  ddp.currentPageID = pageNum
#  print "Exporting page {0} of {1}".format(str(ddp.currentPageID), str(ddp.pageCount))
#  arcpy.mapping.ExportToJPEG(mxd, os.path.join(out_ws, Layers[0].name + str(pageNum) + ".JPEG"), resolution=resolution)
  ```
  ### 3. JPEGbyLayer.py
 ```python
 import arcpy, os, string

# Read the parameter values:
Layername = arcpy. GetParameter(0)
out_ws = arcpy.GetParameterAsText(1)
resolution = arcpy.GetParameterAsText(2)

mxd = arcpy.mapping.MapDocument("CURRENT")
df = mxd.activeDataFrame
ddp = mxd.dataDrivenPages

Layers = arcpy.mapping.ListLayers(Layername, "", df)
#Change title text
TextElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","TitleText")[0]
TextElement.text = Layers[0].name

for pageNum in range(1, ddp.pageCount + 1):
  ddp.currentPageID = pageNum
  print "Exporting page {0} of {1}".format(str(ddp.currentPageID), str(ddp.pageCount))
  arcpy.mapping.ExportToJPEG(mxd, os.path.join(out_ws, Layers[0].name + str(pageNum) + ".jpeg"), resolution=resolution)
del mxd
```



