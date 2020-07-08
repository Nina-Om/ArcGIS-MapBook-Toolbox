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
#ddp.currentPageID = pageNum

#arcpy.RefreshActiveView(),arcpy.RefreshTOC()
arcpy.AddMessage(listlayers)
arcpy.AddMessage(out_ws)

for lyr in listlayers:
  arcpy.AddMessage(lyr)
  lyr = arcpy.mapping.ListLayers(mxd, lyr ,df)[0]
  lyr.visible = True
  arcpy.RefreshActiveView(),arcpy.RefreshTOC()
  TextElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "")
  TextElement[1].text = lyr.name
  TextElement[0].text = lyr.description
  
  tmpPdf = os.path.join(out_ws + os.sep + str(lyr.name) + ".pdf")
  ddp.exportToPDF(tmpPdf, "RANGE", pageRangeString, multipleFiles , res)
  lyr.visible = False
  arcpy.RefreshActiveView(),arcpy.RefreshTOC()

for pageNum in range(1,20):
  if os.path.exists(os.path.join(out_ws + os.sep + "Region" + str(pageNum) + ".pdf")):
   os.remove(os.path.join(out_ws + os.sep + "Region" + str(pageNum) + ".pdf"))
  finalPDF = arcpy.mapping.PDFDocumentCreate(os.path.join(out_ws + os.sep + "Region" + str(pageNum) + ".pdf"))
#  arcpy.AddMessage("Final Report File:" + str(finalPDF))

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
