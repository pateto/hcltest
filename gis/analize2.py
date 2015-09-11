import osgeo.ogr

shapefile = osgeo.ogr.Open("tl_2009_us_state/tl_2009_us_state.shp")
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(2)

print "Feature 2 has the following attributes:"

attributes = feature.items()

for key, value in attributes.items():
	print " %s = %s" % (key, value)	

geometry = feature.GetGeometryRef()
geometryName = geometry.GetGeometryName()

print "Feature's geometry data consists of a %s" % geometryName