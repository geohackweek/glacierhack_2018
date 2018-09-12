# Glacierhack 2018 (Project Title)
DEM differencing and time series analysis

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

# The problem
- Can we quantify inter-annual changes in digital elevation models that represent glacial mass balance?
- Can we improve upon time series analysis methods cappturing changes in digital elevation models (DEMs)?
- What can we learn from image analysis and statistical methods (machine learning), applied to this 4 dimensional array?
- How do our solutions perform at scale? Can we leverage the xarray stack and processing power of a Pangeo? Pangeo is a kubernetes powered jupyterhub configuration that enables distributed data processing and analysis through dask and xarray.

# Relevance (So What? - Application Example)
- Predict the fate of glaciers and impact for water resource management. 
- Explore if methods developed for this dataset can be applied to other glacier systems, such as glaciers that experience periodic surges. 
- Learn new data science methods.

# Dataset
[Khumbu Time Series](https://github.com/geohackweek/glacierhack_2018/wiki/Dataset)

# Specific Questions
- Can we quantify inter-annual changes in digital elevation models that represent glacial mass balance?
- Is the trendfitting of glacial mass change robust to systems that experience high variability? (What kind of math makes sense?) -- math folks
- Can we improve upon time series analysis methods cappturing changes in digital elevation models (DEMs)?
- What can we learn from image analysis and statistical methods (machine learning), applied to this 4 dimensional array?
- How do our solutions perform at scale? Can we leverage the xarray stack and processing power of a Pangeo? Pangeo is a kubernetes powered jupyterhub configuration that enables distributed data processing and analysis through dask and xarray.
- How much water is being released / added to the system?
- Can we calculate velocities from changes in elevation and create a velocity map/vector field for the glacier?

# Proposed methods/tools

## Tools/Libraries
[Relevant python libraries](Resources-for-literature-and-relevant-python-libraries)

## Products
- Notebook for visualization
- Interactive 2D/3D widgets

## Goals
- Explore stacking raster DEMs and conversion to nD xarray object (basic elevation time series manipulations)
- Explore stacking raster DEMs and conversion to Dask array (perform distributed computing)
- Explore bridge between a dataset (Python) and Google Earth Engine (Javascript)

# Background reading
[See the Wiki](Background-reading-and-information)

# Tasks
- Co-register DEMs: Done!
- Write the code to recognize the data files
- Import the data into xarray Dataset list (or equivalent) where elevations can be addressed by (lat, lon) coordinates
- Build a point visualizer: Suggest a Widget tool with lat and lon sliders that plots altitude against time
  - If you are unfamiliar with Python widgets I'm happy to demo
- Build a raster visualizer: Suggest a time widget rendering elevation as color relative to the mean
