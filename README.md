# Glacierhack 2018 (Project Title)
DEM differencing and time series analysis.

# Collaborators
- Elad Dente - Hydro-Geomorphology
- Håvard Holm - Applied Mathematics
- Daniel Howard - Applied Mathematics
- Michelle Hu - Hydrology - Snow Water Runoff
- Lynn Kaack - Applied Mathematics
- Joachim Meyer - Computer Science and Software Development
- Wei Wei - Geophysics - Ice Sheets and Ocean Interactions

## Team Lead
- Shashank Bhushan - Glaciology and Geospatial Image Analysis

## Data Science Lead
- Friedrich Knuth - Data Science Methods and Geospatial Image Analysis

# Dataset
[Khumbu Time Series](https://github.com/geohackweek/glacierhack_2018/wiki/Dataset)

# Problem (What?)
- Can we quantify inter-annual changes in digital elevation models that represent glacial mass balance?
- Is the trendfitting of glacial mass change robust to systems that experience high variability?
- Can we improve upon time series analysis methods cappturing changes in digital elevation models (DEMs)?
- What can we learn from image analysis and statistical methods (machine learning), applied to this 4 dimensional array?
- How do our solutions perform at scale? Can we leverage the xarray stack and processing power of a Pangeo? Pangeo is a kubernetes powered jupyterhub configuration that enables distributed data processing and analysis through dask and xarray.
- How much water is being released / added to the system?
- Can we calculate velocities from changes in elevation and create a velocity map/vector field for the glacier?

# Relevance (So What?)
- Predict the fate of glaciers and impact for water resource management. 
- Explore if methods developed for this dataset can be applied to other glacier systems, such as glaciers that experience periodic surges.
- Learn new data science tools, together.

# Methods (Now What?)
[Tools/Libraries](https://github.com/geohackweek/glacierhack_2018/wiki/Resources-for-literature-and-relevant-python-libraries)

## Goals
- Run pygeotools and raster tutorial workflow on Khumbu dataset. Explore time series analysis. [notebook](https://nbviewer.jupyter.org/github/geohackweek/glacierhack_2018/blob/master/notebooks/0_havard_lynn.ipynb) 
- Read DEMs into Xarray and compare performance to pygeotools operations. [notebook](https://nbviewer.jupyter.org/github/geohackweek/glacierhack_2018/blob/master/final_image_to_xarray-Copy1.ipynb)
- Visualize and extract elevation profiles from DEMs. [notebook](https://nbviewer.jupyter.org/github/geohackweek/glacierhack_2018/blob/master/notebooks/2_michelle_elad.ipynb)
- Create velocity maps from hillshade profiles using vmap and NASA Ames Stereo Pipeline. [notebook](https://nbviewer.jupyter.org/github/weiweiutd/glacierhack_2018/blob/master/notebooks/3_wei_shashank.ipynb)
- Read in DEM data straight from Google Drive without downloading the files. [notebook](https://nbviewer.jupyter.org/github/geohackweek/glacierhack_2018/blob/master/notebooks/4_daniel_friedrich.ipynb)

## Background reading
[See the Wiki](https://github.com/geohackweek/glacierhack_2018/wiki/Background-reading-and-information)
