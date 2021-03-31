"""
A.W. 2021

Run the RFM.
"""


import numpy as np
import climlab
import xarray as xr
import subprocess

def make_driver(outfile=None, fname=None, atmfile, 
                SPC="0.1 3500 0.01",
                OUT=None,):
    """
    
    """
    if fname is None:
        fname = 
    
    with open(fname,"w+") as file:
        file.write("! Produced using rfmtools - Andrew Williams 2021. \n")
        file.write("! andrew.williams@physics.ox.ac.uk \n ")
        
        
    *OUT
    OUTDIR = ./output/
    ABSFIL =  abs_*.asc_test
    TRAFIL =  tra_*.asc_test
    
    return


def 



*HDR
05MAY18 RFM Example: Limb Radiance Calculation
*FLG
   RAD FLX OPT CTM VRT SFC
*SPC
   0.1 3500 0.01
*GAS
   CO2 H2O(CTM)
*ATM
   ../atm/usa.atm
*TAN
  20.0
*HIT
  ../hit/h2o_co2_0-3500cm-1.par
*END


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