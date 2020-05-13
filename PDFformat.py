import arcpy, os, string

# Read the parameter values:
Layername = arcpy. GetParameter(0)
out_ws = arcpy.GetParameterAsText(1)
tmpPdf = arcpy.GetParameterAsText(2)

mxd = arcpy.mapping.MapDocument("CURRENT")
df = mxd.activeDataFrame
ddp = mxd.dataDrivenPages

Layers = arcpy.mapping.ListLayers(Layername, "", df)
#Change title text
TextElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","TitleText")[0]
TextElement.text = Layers[0].name


ddp.exportToPDF(os.path.join(out_ws , tmpPdf + ".pdf"), "ALL")
#tmpPdf.appendPages(os.path.join(out_ws , tmpPdf + ".pdf"))
del mxd
tmpPdf.updateDocProperties(pdf_open_view="USE_THUMBS",
pdf_layout="SINGLE_PAGE")
del tmpPdf