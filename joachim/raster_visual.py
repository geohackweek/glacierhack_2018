import glob
import os

import gdal
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from pygeotools.lib import iolib, warplib, geolib, timelib


class RasterFile(object):
    def __init__(self, filename):
        self.file = filename
        self._extent = None
        self._elevation = None

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, filename):
        self._file = gdal.Open(filename)

    @property
    def extent(self):
        if self._extent is None:
            gt = self.geo_transform()
            x_min = gt[0]
            x_max = gt[0] + self.file.RasterXSize / gt[1]
            y_min = gt[3] + self.file.RasterYSize / gt[5]
            y_max = gt[3]

            self._extent = x_min, x_max, y_min, y_max
        return self._extent

    @staticmethod
    def get_values_for_raster(raster, band_number=1):
        band = raster.GetRasterBand(band_number)
        values = np.ma.masked_values(
            band.ReadAsArray(), band.GetNoDataValue() or 0., copy=False
        )
        del band
        return values

    def get_raster_attribute(self, attribute):
        raster = gdal.DEMProcessing('', self.file, attribute, format='MEM')
        raster_values = self.get_values_for_raster(raster)
        del raster
        return raster_values

    @property
    def elevation(self):
        if self._elevation is None:
            self._elevation = self.get_values_for_raster(self.file)
        return self._elevation

    @property
    def hill_shade(self):
        return self.get_raster_attribute('hillshade')

    def geo_transform(self):
        return self.file.GetGeoTransform()


class RasterSource(object):
    FILE_ENDING = 'trans.tif'

    def __init__(self, folder):
        self._folder = folder

    def file_list(self):
        return glob.glob(
            os.path.join(self._folder, '') + '**/*' + self.FILE_ENDING,
            recursive=True
        )


if __name__ == '__main__':
    files = RasterSource(
        '/Volumes/warehouse/projects/UofU/geohackweek/galcier_data/khumbu_DEM_32m/'
    ).file_list()

    raster_list = warplib.memwarp_multi_fn(
        files, extent='union', res='min', t_srs=files[0]
    )

    band_data = [iolib.ds_getma(i).filled(np.NaN) for i in raster_list]

    x, y = geolib.get_xy_grids(raster_list[0])
    time_list = np.array([timelib.fn_getdatetime(fn) for fn in files])

    x_band_data = xr.DataArray(
        np.stack(band_data),
        coords={
            'lat': y[::,0],
            'lon': x[0,::],
            'time': time_list
        },
        dims=('time', 'lat', 'lon'),
        name='elevation'
    )

    x_band_data = x_band_data.sortby('time')

    x_band_data['mean'] = x_band_data.mean(dim=('lat', 'lon'))
    x_band_data['count'] = x_band_data.count(dim='time')

    x_band_data['count'].plot()

    plt.show()

