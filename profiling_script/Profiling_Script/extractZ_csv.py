#! /usr/bin/env python

'''
David Shean
dshean@gmail.com
3/21/12

#NOTE: Fails to preserve strings in input csv

To do:
Mask support?
Use appropriate spot size for ATM/ICESat points, extract gaussian
'''


import sys, os
import csv
import argparse

from osgeo import gdal, ogr, osr

import numpy as np
import scipy.ndimage
import scipy.interpolate

from pygeotools.lib import malib, geolib
#from lib import geolib

#Note: can also directly read from GDAL ds instead of from array, although likely much slower when not in memory
#ds.ReadAsArray(x,y,1,1)

#extract Z value for single pixel or for coordinate arrays
#Input is assumed to be masked array
def extractPoint(b, x, y):
    #Note: simplest way using integer indices 
    x = np.clip(x, 0, b.shape[1] - 1)
    y = np.clip(y, 0, b.shape[0] - 1)
    
    return b[np.ma.around(y).astype(int), np.ma.around(x).astype(int)]
    
    #Interpolate values for sub-pixel indices
    #return geolib.bilinear(x, y, b, gt)
   
    #The following is the ideal way to do this
    #Unfortunately, doesn't work for nan
    #http://projects.scipy.org/scipy/ticket/1155
    #return malib.nanfill(b, scipy.ndimage.interpolation.map_coordinates, [y, x], cval=b.fill_value) 
    #Creates bogus values near edges
    #return scipy.ndimage.interpolation.map_coordinates(b, [y, x], cval=b.fill_value) 

#Compute sum of mask for window around each point
#If >50%, do interpolation

def extractPoint_interp2d(b, x, y):
    #Can do this for the full x, y domain
    #http://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array
    #
    return None


#Interpolate using only valid data
def extractPointSBS(b, x, y):
    idx = b.filled(0).nonzero()
    X = idx[0]
    Y = idx[1]
    Z = b.compressed()
    #Degrees of bivariate spline
    k = 3
    #Smoothing factor
    s = 0
    #Can also specify bbox
    sp = scipy.interpolate.SmoothBivariateSpline(X, Y, Z, kx=k, ky=k, s=s)
    #sp = scipy.interpolate.LinearNDInterpolator(np.hstack(X, Y), Z)
    return sp(x, y)

#Interpolate values from regular grid
def extractPointRBS(b, x, y):
    X = np.arange(b.shape[0])
    Y = np.arange(b.shape[1])
    #Degrees of bivariate spline
    k = 3
    #Smoothing factor
    s = 0
    #This still has issues with masked data
    #Need to use b.filled here?
    #Can also specify bbox
    sp = scipy.interpolate.RectBivariateSpline(X, Y, b, kx=k, ky=k, s=s)
    return sp(x, y)

#extract Z value for block with dimensions rx, ry
def extractBlock(b, x, y, rx, ry):
    #Want to make sure extended kernel isn't outside array bounds
    y = np.around(y).astype(int)
    x = np.around(x).astype(int)
    kernel = b[y-ry:y+ry,x-rx:x+rx]
    #return np.median(kernel)
    return np.ma.median(kernel.compressed())

#Generate histogram
def genhist(b):
    import matplotlib.pyplot as plt
    plt.figure()
    n, bins, patches = plt.hist(b, 512) 
    plt.xlabel('Elevation Difference (m)')
    plt.ylabel('Count')
    plt.xlim(-20, 20)
    plt.grid(True)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Utility to extract raster values')
    #Add x, y, z column definitions as optional arguments (defaults 0, 1, 2)
    parser.add_argument('feat_fn', help='input feature filename "points.csv"')
    parser.add_argument('filelist', nargs='+', help='input filenames "img1.tif img2.tif..."') 
    args = parser.parse_args()

    #Assumptions
    #Input csv has x,y,z as first three columns
    #cat jako_icesat_clip.csv | awk -F',' 'BEGIN {OFS=","} { print $8, $9, $1, $2}'
    #Input xyz coordinates have identical projection to input rasters

    #For input csv containing x,y,z coordinates
    #Load into np array
    ndv = np.nan
    #Expects column names in first line header
    #a = np.genfromtxt(args.feat_fn, delimiter=',', names=True)
    #a_ma = np.ma.masked_equal(a.view((np.float, len(a.dtype.names))), ndv)
    #header = list(a.dtype.names)
    a = np.genfromtxt(args.feat_fn, delimiter=',', dtype=None)
    a_ma = np.ma.masked_equal(a, ndv)
    header = ['x','y','z']

    #Grab header as separate list 
    #with open(args.feat_fn, 'r') as f:
    #    reader = csv.reader(f)
    #    header = reader.next()
    #Now loads directly into 2d np array
    #a = np.loadtxt(args.feat_fn, delimiter=',', skiprows=1)

    #check number of records
    if a_ma.shape[0] == 0: 
        sys.exit('Input csv contains no records')
   
    #Try to find columns with lon or [Xx]
    #Check to see if we have a z column, or multiple z columns
            
    #If x,y,z columns are specified, use those indices
    #xidx = -2 
    xidx = 0 
    #yidx = -1
    yidx = 1
    #zidx = None
    zidx = 2 
   
    #Use this with array imported with genfromtxt 
    #xcol = a_ma[a_ma.dtype.names[0]]
    #ycol = a_ma[a_ma.dtype.names[1]]
    #zcol = a_ma[a_ma.dtype.names[2]]

    #Keep everything in the output array
    out_ma = a_ma
    out_ndv = np.nan
    #out_ndv = -32768

    #x, y, z
    fmt = ['%0.6f', '%0.6f']
 
    for fn in args.filelist:
        #Want to reload these, as they are overwritten if coordTransform
        #Use this with array imported with loadtxt
        xcol = a_ma[:,xidx]           
        ycol = a_ma[:,yidx]           
        if zidx is not None:
            zcol = a_ma[:,zidx]           
            fmt.append('%0.3f')

        #These short names are useless
        #DEM mosaics, use date
        #create dictionary, output key with full filenames
       
        #Apply smoothing filter to input datasets
        #This can be done on the fly, but some ds are very large, so write out product
        smooth = False 
        if smooth:
            b_smooth_fn = os.path.splitext(fn)[0]+'_smooth.tif'
            if os.path.exists(b_smooth_fn):
                fn = b_smooth_fn
            else:
                """
                print 'Smoothing %s' % fn
                from lib import filtlib 
                size = 9
                ds = gdal.Open(fn, gdal.GA_ReadOnly)
                #This should be done for each band number bn
                #For now, just assume singleband
                bn = 1
                b = malib.fn_getma(fn)
                b_smooth = filtlib.gauss_fltr_astropy(b, size=size)
                malib.writeGTiff(b_smooth, b_smooth_fn, ds, bnum=bn) 
                #b = b_smooth
                fn = b_smooth_fn
                """

        shortName = fn[:8]
        ds = gdal.Open(fn, gdal.GA_ReadOnly)
        gt = ds.GetGeoTransform()
        res = (gt[1] - gt[5]) / 2
        rasterCRS = osr.SpatialReference()
        rasterCRS.ImportFromWkt(ds.GetProjectionRef())
    
        #Assume that input csv has same projection
        layerCRS = rasterCRS
        #layerCRS = geolib.wgs_srs 

        coordTransform = None
        if not layerCRS.IsSame(rasterCRS):
            #Faster to use pyproj here?
            coordTransform = osr.CoordinateTransformation(layerCRS, rasterCRS)
            mapcoord = np.array([coordTransform.TransformPoint(x, y, 0) for x,y in zip(xcol, ycol)])
            #xcol, ycol, zcol = zip(*mapcoord) 
            xcol, ycol, zcol = np.hsplit(mapcoord, 3) 
        
        for bn in range(1, ds.RasterCount+1):
            print fn, bn
            b = malib.ds_getma(ds, bn) 
            #Note, ndv should be universal, so output values are consistent
            ndv = b.fill_value
 
            rzcol = np.empty(xcol.shape)
            rzcol[:] = ndv

            #This uses np index arrays to do the extraction - very fast
            if True:
                #This may be off by one
                #Getting some errors IndexError: index (14187) out of range (0<=index<14186) in dimension 1
                pX, pY = geolib.mapToPixel(xcol, ycol, gt)
                #Need some kind of check here for pX and pY
                #if (pX.min() < 0 or pX.max() >= ds.RasterXSize) or (pY.min() < 0 or pY.max() >= ds.RasterYSize):
                #But how to preserve record with ndv using index arrays?  
                #Could use masked arrays with fill values of 0,0 - assume that 0,0 will be nodata in input raster?
                #DONT use ma here
                pX = np.clip(pX, 0, ds.RasterXSize-1)
                pY = np.clip(pY, 0, ds.RasterYSize-1)
                #pX = np.ma.masked_outside(np.ma.around(pX), 0, ds.RasterXSize-1)
                #pY = np.ma.masked_outside(np.ma.around(pY), 0, ds.RasterYSize-1)
                rzcol = extractPoint(b, pX, pY) 
            
            #This goes through record by record and extracts values
            #Safer for ndv handling and exceptions beyond b extent
            else:
                for i in range(xcol.size):
                    x = xcol[i]
                    y = ycol[i]
                    
                    #Need to vectorize this to process entire array up front
                    if coordTransform is not None:
                        cT = coordTransform.TransformPoint(x, y, z)
                        x = cT[0]
                        y = cT[1]
                   
                    #Create index arrays
                    pX, pY = geolib.mapToPixel([x], [y], gt)
                 
                    #Make sure pixel location is within map coordinates
                    if (pX < 0 or pX >= ds.RasterXSize) or (pY < 0 or pY >= ds.RasterYSize):
                        rz = out_ndv
                    else:
                        #Extract Z value at a single pixel
                        rz = extractPoint(b, pX, pY)

                        #Pull out instrument ID and add logic for block size
                        #ICESat is ~70 m diameter for early shots, ~35 m diameter for later shots
                        #block_m = np.array([35, 35])
                        #ATM L2 is roughly 50 m along-track and 80 m cross-track
                        #Need to compute heading to properly sample these blocks, for now assume diameter 50 m
                        #block_m = np.array([25, 25])
                        #block_p = np.around(block_m/res)
                        #rz = extractBlock(b, pX, pY, block_p[0], block_p[1])
                    rzcol[i] = rz

            #rzcol = np.ma.fix_invalid(rzcol, copy=False)
            #This is necessary b/c np.nan is float, can't set fill for int
            rzcol = np.ma.fix_invalid(rzcol, copy=False).astype(np.float)
            rzcol.set_fill_value(out_ndv)
            
            #Use shortname for shp
            #colname = shortName + '_b' + str(bn)
           
            colname = os.path.splitext(os.path.split(fn)[1])[0]+'_b'+str(bn) 
            header.append(colname)
            out_ma = np.ma.column_stack((out_ma, rzcol))
            fmt.append('%0.3f')
            
            #Compute difference values
            if zidx is not None:
                dzcol = zcol - rzcol
                dzcol.set_fill_value(out_ndv)
                stats = malib.print_stats(dzcol)
                genhist(dzcol)
                header.append(colname + '_dz')
                out_ma = np.ma.column_stack((out_ma, dzcol))
                fmt.append('%0.3f')
        b = None
    ds = None

    dst_fn = os.path.splitext(args.feat_fn)[0]+'_extractZ.csv'
    f = open(dst_fn, 'w')
    writer = csv.writer(f)
    writer.writerow(header)
    #np.savetxt(f, out_ma, delimiter=",", fmt=fmt)
    np.savetxt(f, out_ma, delimiter=",", fmt=('%0.6f'))
    f.close()

if __name__ == '__main__':
    main()
