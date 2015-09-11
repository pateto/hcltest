import osgeo.ogr
import pdb

def findPoints(geometry, results):
	#pdb.set_trace()
	for i in range(geometry.GetPointCount()):
		x,y,z = geometry.GetPoint(i)
		if results['north'] == None or results['north'][1] < y:
			results['north'] = (x,y)
		if results['south'] == None or results['south'][1] > y:
			results['south'] = (x,y)
	for i in range(geometry.GetGeometryCount()):		
		findPoints(geometry.GetGeometryRef(i), results)

shapefile = osgeo.ogr.Open("tl_2009_us_state/tl_2009_us_state.shp")

layer = shapefile.GetLayer(0)
feature = layer.GetFeature(53)
geometry = feature.GetGeometryRef()
results = {'north' : None, 'south' : None}
findPoints(geometry, results)
print "Northernmost point is (%0.4f, %0.4f)" % results['north']
print "Southernmost point is (%0.4f, %0.4f)" % results['south']