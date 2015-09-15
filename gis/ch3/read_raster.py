from osgeo import gdal, gdalconst
import struct
import pdb

pdb.set_trace()
dataset = gdal.Open("1.tif")
band = dataset.GetRasterBand(1)
#band.ReadAsArray()

fmt = "<" + ("h" * band.XSize)
totHeight = 0
for y in range(band.YSize):
	scanline = band.ReadRaster(0, y, band.XSize, 1, band.XSize, 1, band.DataType)
	values = struct.unpack(fmt, scanline)
	for value in values:
		totHeight = totHeight + value
	average = totHeight / (band.XSize * band.YSize)
print "Average height =", average