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
  arcpy.mapping.ExportToPNG(mxd, os.path.join(out_ws, Layers[0].name + str(pageNum) + ".png"), resolution=resolution)
del mxd
