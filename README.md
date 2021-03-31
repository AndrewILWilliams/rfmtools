rfmtools
************************************************

Created/Mantained By: Andrew Williams (andrew.williams@physics.ox.ac.uk)
Other Contributors: ()

### Features
===================
 * Easily generate idealized atmospheric profiles of H2O, CO2 and temperature, in an RFM-friendly format.
 * Run the RFM from within a jupyter notebook!
 * Directly parses output files into `xr.DataArray`s!
 
 
### Installation
===================

An `environment.yml` file is provided from which you can generate an `rfm` environment with the command `conda env create --file environment.yml`. 

To add this environment to you `jupyter lab` instance, you must first activate this environment and then run `ipython kernel install --user --name=rfm`.

