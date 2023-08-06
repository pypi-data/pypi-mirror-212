# -*- coding: utf-8 -*-

import os
import csv
import warnings
import numpy as np
import shapefile
from osgeo import osr, gdal

class GeoMetadata:
    def __init__(self):
        self.projection = None
        self.geotransform = None
        self.rasterXY = None

# Read metadata from a geotiff file
def loadGeoMetadata(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f'The file {filename} does not exist.')
    else:
        ds = gdal.Open(filename)

        if ds is None:
            raise ValueError('Unable to read file.')

        georefmtd = GeoMetadata()
        georefmtd.projection   = ds.GetProjection()
        georefmtd.geotransform = ds.GetGeoTransform()
        georefmtd.rasterXY = (ds.RasterXSize, ds.RasterYSize)

        if georefmtd.projection is None:
            warnings.warn('No projection found in the metadata.')
    
        if georefmtd.geotransform is None:
            warnings.warn('No geotransform found in the metadata.')

        # Close file
        del ds

        return georefmtd

# Save a raster image as a geotiff file
def saveAsGeoTiff(georefmtd, rasterimg, filename):

    if not os.path.exists(filename):
        raise FileNotFoundError(f'The file {filename} does not exist.')
    else:

        if (rasterimg.shape[1] != georefmtd.rasterXY[0]) and (rasterimg.shape[0] != georefmtd.rasterXY[1]):
            raise ValueError('Image size does not match the metadata')

        DATA_TYPE = {
          "uint8": gdal.GDT_Byte,
          "int8": gdal.GDT_Byte,
          "uint16": gdal.GDT_UInt16,
          "int16": gdal.GDT_Int16,
          "uint32": gdal.GDT_UInt32,
          "int32": gdal.GDT_Int32,
          "float32": gdal.GDT_Float32,
          "float64": gdal.GDT_Float64
        }

        driver = gdal.GetDriverByName('GTiff')
    
        ds = driver.Create(filename, rasterimg.shape[1], rasterimg.shape[0], 1, DATA_TYPE[rasterimg.dtype.name])

        ds.SetGeoTransform(georefmtd.geotransform)
        ds.SetProjection(georefmtd.projection)
        ds.GetRasterBand(1).WriteArray(rasterimg)
        ds.FlushCache()

        # Close file
        del ds

# Convert pixel coordinates into longitude and latitude
def pix2lonlat(georefmtd, x, y):

    sr = osr.SpatialReference()
    sr.ImportFromWkt(georefmtd.projection)
    ct = osr.CoordinateTransformation(sr,sr.CloneGeogCS())

    lon_p = x*georefmtd.geotransform[1]+georefmtd.geotransform[0]
    lat_p = y*georefmtd.geotransform[5]+georefmtd.geotransform[3]

    lon, lat, _ = ct.TransformPoint(lon_p, lat_p)

    return lon, lat

# Convert longitude and latitude into pixel coordinates
def lonlat2pix(georefmtd, lon, lat):

    sr = osr.SpatialReference()
    sr.ImportFromWkt(georefmtd.projection)
    ct = osr.CoordinateTransformation(sr.CloneGeogCS(),sr)

    lon_p, lat_p, _ = ct.TransformPoint(lon, lat)
    x = (lon_p - georefmtd.geotransform[0]) / georefmtd.geotransform[1]
    y = (lat_p - georefmtd.geotransform[3]) / georefmtd.geotransform[5]

    return int(x), int(y)

# Export (coordinate, width) pairs to a CSV file
def exportCSVfile(centerlines, widthMap, georefmtd, filename):

    centerlineWidth = widthMap[centerlines]
    [row,col] = np.where(centerlines)

    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["width","lat","lon"])

        for i in range(0, len(centerlineWidth)):
            lon, lat = pix2lonlat(georefmtd, col[i], row[i])
            writer.writerow([centerlineWidth[i], lat, lon])

# Export line segments to a ShapeFile
def exportShapeFile(centerlines, widthMap, georefmtd, filename):

    # initiate the shp writer
    w = shapefile.Writer(filename)
    w.field('width', 'N', decimal=2)

    R, C = centerlines.shape

    # make a copy of the centerlines matrix since we'll be modifying it
    c_copy = centerlines.copy()

    # scan the centerline matrix skipping the boundary pixels
    # convert neighbor centerline pixels into line segments
    for r in range(1, R-1):
        for c in range(1, C-1):
            if c_copy[r,c]:
                c_copy[r,c] = 0
                lon_orig, lat_orig = pix2lonlat(georefmtd, c, r)

                # connect neighbors (check diagonals first)
                if c_copy[r-1, c-1]:
                    c_copy[r-1, c] = 0
                    c_copy[r, c-1] = 0
                    lon, lat = pix2lonlat(georefmtd, c-1, r-1)
                    width = ( + widthMap[r-1, c-1]) / 2
                    w.record(width)
                    w.line([[[lon_orig, lat_orig], [lon, lat]]])

                if c_copy[r-1, c+1]:
                    c_copy[r-1, c] = 0
                    c_copy[r, c+1] = 0
                    lon, lat = pix2lonlat(georefmtd, c+1, r-1)
                    width = (widthMap[r, c] + widthMap[r-1, c+1]) / 2
                    w.record(width)
                    w.line([[[lon_orig, lat_orig], [lon, lat]]])

                if c_copy[r+1, c-1]:
                    c_copy[r+1, c] = 0
                    c_copy[r, c-1] = 0
                    lon, lat = pix2lonlat(georefmtd, c-1, r+1)
                    width = (widthMap[r, c] + widthMap[r+1, c-1]) / 2
                    w.record(width)
                    w.line([[[lon_orig, lat_orig], [lon, lat]]])

                if c_copy[r+1, c+1]:
                    c_copy[r+1, c] = 0
                    c_copy[r, c+1] = 0
                    lon, lat = pix2lonlat(georefmtd, c+1, r+1)
                    width = (widthMap[r, c] + widthMap[r+1, c+1]) / 2
                    w.record(width)
                    w.line([[[lon_orig, lat_orig], [lon, lat]]])

                if c_copy[r-1, c]:
                    lon, lat = pix2lonlat(georefmtd, c, r-1)
                    width = (widthMap[r, c] + widthMap[r-1, c]) / 2
                    w.record(width)
                    w.line([[[lon_orig, lat_orig], [lon, lat]]])

                if c_copy[r+1, c]:
                    lon, lat = pix2lonlat(georefmtd, c, r+1)
                    width = (widthMap[r, c] + widthMap[r+1, c]) / 2
                    w.record(width)
                    w.line([[[lon_orig, lat_orig], [lon, lat]]])

                if c_copy[r, c-1]:
                    lon, lat = pix2lonlat(georefmtd, c-1, r)
                    width = (widthMap[r, c] + widthMap[r, c-1]) / 2
                    w.record(width)
                    w.line([[[lon_orig, lat_orig], [lon, lat]]])

                if c_copy[r, c+1]:
                    lon, lat = pix2lonlat(georefmtd, c+1, r)
                    width = (widthMap[r, c] + widthMap[r, c+1]) / 2
                    w.record(width)
                    w.line([[[lon_orig, lat_orig], [lon, lat]]])

    w.close()
