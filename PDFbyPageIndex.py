import arcpy, os, string, os.path

# Read the parameter values:
listlayers = arcpy.GetParameter(0)
out_ws = arcpy.GetParameterAsText(1)
pageNum = arcpy.GetParameter(2)

mxd = arcpy.mapping.MapDocument("CURRENT")
df = mxd.activeDataFrame
ddp = mxd.dataDrivenPages
ddp.currentPageID = pageNum
arcpy.AddMessage(listlayers)
arcpy.AddMessage(out_ws)

for lyr in listlayers:
  arcpy.AddMessage(lyr)
  lyr = arcpy.mapping.ListLayers(mxd, lyr ,df)[0]
  lyr.visible = True
  arcpy.RefreshActiveView(),arcpy.RefreshTOC()
  tmpPdf = os.path.join(out_ws + "\\"+ str(lyr.name) + str(pageNum) + ".pdf")

  TextElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TitleText")[0]
  TextElement.text = lyr.name
  ddp.exportToPDF(tmpPdf, "CURRENT")
  lyr.visible = False
  arcpy.RefreshActiveView(),arcpy.RefreshTOC()

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