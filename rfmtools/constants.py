import numpy as np
import climlab
import xarray as xr


eps   = 0.622 # molar mass ratio of vapour to total moist air
L     = 2260000 # Latent heat of vap, water, J/kg

R_a   = 287.058 # gas constant for dry air, J/kg/K
R_c   = 461.5  # gas constant for water vapour, J/kg/K
cp_a  = 1004 # specific heat capacity of air, J/kg/K 

g = 9.81 # m/s2