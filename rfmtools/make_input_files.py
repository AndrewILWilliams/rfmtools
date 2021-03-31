"""
A.W. 2021

Set of functions to generate temperature/pressure/height/H2O grids to input into RFM.
"""


import numpy as np
import climlab
import xarray as xr


def generate_atm_file(fname, height, temp, pres, h2o, co2):
    """
    Generate a .atm input file for RFM
    """
    nz = int(len(height))
    
    variables = [height, pres, temp, h2o, np.ones(nz)*co2] 
    
    labels=["*HGT [km]","*PRE [mb]","*TEM [K]","*H2O [ppmv]","*CO2 [ppmv]"]
    
    with open(fname,"w+") as file:
        file.write("! Produced using rfmtools - Andrew Williams 2021. \n")
        file.write("! andrew.williams@physics.ox.ac.uk \n ")
        
        file.write(f" {nz} ! No.Levels in profiles \n")
        
        for idx, label in enumerate(labels):
            file.write(f" {label} \n")
            x=",       ".join([str(i) for i in variables[idx]])
            file.write(f" {x} \n")
        file.write("*END")