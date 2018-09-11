# glacierhack_2018
DEM differencing and time series analysis

# Data
Khumbu time series: https://drive.google.com/drive/folders/0B5c3UTO8DDZwdmpYaFlXa1BkM0U?usp=sharing

Composite DEM at 8-m posting for full area:
- hma_20170716_mos_8m_warp_dzfilt_0.00-100.00_gaussfill-tile-0.tif

Contents of dem_coreg subdirectory (output from pc_align co-registration):
- Co-registered DEMs at 2, 8 and 32 m posting: *_2m_trans.tif
- Shaded relief maps (illumination from NW, azimuth of 315 degrees): *_hs_az315.tif
- Multidirecitonal shaded relief maps: *hs_multi.tif

Example filename:
- 20161105_0448_1050010007140900_1050010007140B00-DEM_8m_trans.tif
- YYYYmmdd_HHMM_catalogid1_catalogid2

See NSIDC page for additional details: 
- https://nsidc.org/data/HMA_DEM8m_AT/versions/1#title0
- https://nsidc.org/data/HMA_DEM8m_CT/versions/1#title0
- https://nsidc.org/data/HMA_DEM8m_MOS/versions/1#title0

# Tasks

- Co-register DEMs: Done!
- Write the code to recognize the data files
- Import the data into xarray Dataset list (or equivalent) where elevations can be addressed by (lat, lon) coordinates
- Build a point visualizer: Suggest a Widget tool with lat and lon sliders that plots altitude against time
  - If you are unfamiliar with Python widgets I'm happy to demo
- Build a raster visualizer: Suggest a time widget rendering elevation as color relative to the mean
