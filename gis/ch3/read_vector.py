from osgeo import ogr

shapefile = ogr.Open("TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)
for i in range(layer.GetFeatureCount()):
	feature = layer.GetFeature(i)
	name = feature.GetField("NAME")
	geometry = feature.GetGeometryRef()
	print i, name, geometry.GetGeometryName()