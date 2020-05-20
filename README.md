# ArcGIS-MapBook-Toolbox

MapBook.tbx contains three script files to automate ArcGIS maps production:<br />
 1. PDFbyPageIndex.py  <br />For producing single page PDF files of the selected layers for one Data Driven Page Number as well as the   appended PDF file of the selected layers <br /> 
 2. PDF_byLayer.py  <br />For producing appended PDF file of a selected layer for ALL Data Driven pages <br />
 3. JPEGbyPageIndex  <br />For producing a JPEG file of the selected layers for one Data Driven Page Number <br />

The current scripting Toolbox, MapBook, enables to include dynamic data frame title, continuous page number for all of the target layers, setting the print properties and generating PDF and PNG files of the selected target data layers with the aid of Data Driven Pages and Arcpy.mapping. The output files should be saved in the separate folders based on the selected Data Driven Page number.

To use this toolbox, the Data Driven Pages and laout should be defined in mapdocument environment. Data Driven Pages Tutorial is available at [Data Driven Pages](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00sr00000006000000).


![alt text here](https://github.com/Nina-Om/ArcGIS-MapBook-Toolbox/blob/master/toolbox2.PNG)

![alt text here](https://github.com/Nina-Om/ArcGIS-MapBook-Toolbox/blob/master/pdf1.PNG)

![alt text here](https://github.com/Nina-Om/ArcGIS-MapBook-Toolbox/blob/master/pdf2.PNG)

![alt text here](https://github.com/Nina-Om/ArcGIS-MapBook-Toolbox/blob/master/jpeg.PNG)


## MapDocument

Map scripting can be integrated with Data Driven Pages to create a map book that includes custom maps on different pages while using a single map document. In order to use Data Driven Pages to build a map book you need to use Arcpy.mapping. This module provides functions to automate exporting and printing. Arcpy.mapping was designed primarily to manipulate the contents of existing map documents (.mxd) and layer files (.lyr). It also provides functions to automate exporting and printing. Arcpy.mapping can be used to automate map production; it extends the capabilities of Data Driven Pages and is required to build complete map books because it includes functions to export to, create, and manage PDF documents.

## Links for more information
[Data Driven Pages](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00sr00000006000000)<br />
[Arcpy.mapping](https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/introduction-to-arcpy-mapping.htm)<br />
[Relevant blog post](https://www.esri.com/arcgis-blog/products/arcgis-desktop/mapping/combining-data-driven-pages-with-python-and-arcpy-mapping/)<br />
[MapDocument](https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/mapdocument-class.htm)



## Usage
Before using the toolbox:

Please set up Data Driven Pages before using the tool. As well as the map title, legend, etc. 

Please define the map tiltle Element Name as 'TitleText' before using the tool. You should open your map title properties, click on "Size and Position" Tab and type "TitleText" in "Element name" box.

![alt text here](https://github.com/Nina-Om/ArcGIS-MapBook-Toolbox/blob/master/Capture.PNG)


## Python Scripts
### 1. PDFbyPageIndex.py

```python
import arcpy, os, string

# Read the parameter values:
listlayers = arcpy.GetParameter(0)
out_ws = arcpy.GetParameterAsText(1)
pageNum = arcpy.GetParameter(2)
#
mxd = arcpy.mapping.MapDocument("CURRENT")
df = mxd.activeDataFrame
ddp = mxd.dataDrivenPages
ddp.currentPageID = pageNum
arcpy.AddMessage(listlayers)
arcpy.AddMessage(out_ws)
# 
for lyr in listlayers:
  arcpy.AddMessage(lyr)
  lyr = arcpy.mapping.ListLayers(mxd, lyr ,df)[0]
  lyr.visible = True
  arcpy.RefreshActiveView(),arcpy.RefreshTOC()
  tmpPdf = os.path.join(out_ws + "\\"+ str(lyr.name) + str(pageNum) + ".pdf")
```
Assign a layer name to dataframe title. Define dataframe `df` Title Element name as `TitleText` in your mapdocument.
```python
  TextElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TitleText")[0]
  TextElement.text = lyr.name
```
Export PDF files of the selected page index 'pageNum'.
```python
  ddp.exportToPDF(tmpPdf, "CURRENT")
  lyr.visible = False
  arcpy.RefreshActiveView(),arcpy.RefreshTOC()
```
Save the PDF files in created workspace 'out_ws' and append the files to a final PDF file 'Region + str(pageNum) + "pdf"'. Foe each DDP Number please save the files in the separate folders.
```python
if os.path.exists(os.path.join(out_ws + "\\" + "Region" + str(pageNum) + ".pdf")):
  os.remove(os.path.join(out_ws + "\\" + "Region" + str(pageNum) + ".pdf"))
finalPDF = arcpy.mapping.PDFDocumentCreate(os.path.join(out_ws + "\\" + "Region" + str(pageNum) + ".pdf"))
arcpy.AddMessage("Final Report File:" + str(finalPDF))

for root, dirs, files in os.walk(out_ws):
 for file in files:
  finalPDF.appendPages(os.path.join(out_ws + "\\" + file))

finalPDF.updateDocProperties(pdf_open_view="USE_THUMBS",
pdf_layout="SINGLE_PAGE")
finalPDF.saveAndClose()
arcpy.AddMessage("________________________________")
arcpy.AddMessage("***PDF files merged successfulley!***")
del mxd
```
### 2. PDF_byLayer.py

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
The next two line change map title automatically based on the layer name. 
```python
TextElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","TitleText")[0]
TextElement.text = Layers[0].name
```
Export ALL `ddp` pages to pdf file `tmpPDF`.
```python
ddp.exportToPDF(os.path.join(out_ws , tmpPdf + ".pdf"), "ALL")
#tmpPdf.appendPages(os.path.join(out_ws , tmpPdf + ".pdf"))
del mxd
tmpPdf.updateDocProperties(pdf_open_view="USE_THUMBS",
pdf_layout="SINGLE_PAGE")
del tmpPdf
```

### 3. JPEGbyPageIndex.py
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
  ```
  



