import arcpy, os, string

# Read the parameter values:
listlayers = arcpy. GetParameter(0)
out_ws = arcpy.GetParameterAsText(1)
resolution = arcpy.GetParameterAsText(2)
pageNum = arcpy.GetParameter(3)

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

