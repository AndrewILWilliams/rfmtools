"""
A.W. 2021

Set of functions to generate input files for RFM.
"""


import numpy as np
import climlab
import xarray as xr
from .utils import RFM_DIR 
import time

def generate_atm_file(fname, height, temp, pres, h2o, co2):
    """
    Generate a .atm input file for RFM.
    
    Inputs:
    * co2: (`int`)
        integer value for CO2 in ppmv, assumed constant with height
    """
    nz = int(len(height))
    
    variables = [height, pres, temp, h2o, np.ones(nz)*co2] 
    
    labels=["*HGT [km]","*PRE [mb]","*TEM [K]","*H2O [ppmv]","*CO2 [ppmv]"]
    
    with open(RFM_DIR+"/atm/"+fname,"w+") as file:
        file.write("! Produced using rfmtools - Andrew Williams 2021. \n")
        file.write("! andrew.williams@physics.ox.ac.uk \n ")
        
        file.write(f" {nz} ! No.Levels in profiles \n")
        
        for idx, label in enumerate(labels):
            file.write(f"{label} \n")
            x=",       ".join([str(i) for i in variables[idx]])
            file.write(f" {x} \n")
        file.write("*END")
    file.close()
        
        
def make_driver(
    runtype='radiance',
    extra_flags=None,
    fname=None, atmfile=None, 
    SPC="0.1 3500 0.1",
    GAS="CO2 H2O",
    HIT=None,
    HDR=None,
    OUTDIR=None,
    NLEV=None):
    """
    Depending on `genre`, we'll expect a certain number of flags to be present...
    Maybe make flags an input LIST???
    
    * runtype: 'optical_depth' or 'radiance'
        sets the default flags
    
    * extra_flags: (`str`)
        For setting additional flags, e.g. 'CTM'
         
    """
    import os
    if runtype=='radiance':
        flags="RAD FLX SFC"
    elif runtype=='optical_depth':
        flags="OPT"
        
    if fname is None:
        raise ValueError("Need to specify a filename, `fname`.") 
        
    # Check atmfile is present, and that it's an absolute path
    if atmfile is None:
        raise ValueError("Oops! You need to specify a `.atm` input file!") 
        
    elif not os.path.isabs(atmfile):
        atmfile=RFM_DIR+"/atm/"+atmfile
    
    # Make sure HITRAN2016 data is there
    if HIT is None:
        HIT=f"{RFM_DIR}/hit/h2o_co2_0-3500cm-1.par"
    
    # Give it a name
    if HDR is None:
        HDR="AW2021: RFM"
    
    if OUTDIR is None:
        stamp = time.time()*1e5
        x = RFM_DIR+"/outp/"+"tmp_%.0f/" % stamp
        OUTDIR="  OUTDIR = "+x # create a unique tmp dir
        os.mkdir(x)
    
    if NLEV is None:
        fp = open(atmfile)
        for i, line in enumerate(fp):
            if line[0:9]=='*PRE [mb]':
                LEV_idx = i-1
            else:
                continue
        fp.close()

        fp = open(atmfile)
        LEV = fp.readlines()[LEV_idx].split()[-1]
        
    # Make flags!
    labels={}
    labels["*HDR"] = HDR
    labels["*FLG"] = flags
    labels["*SPC"] = SPC
    labels["*GAS"] = GAS
    labels["*ATM"] = atmfile
    labels["*LEV"] = LEV
    labels["*HIT"] = HIT
    labels["*OUT"] = OUTDIR
    
    # Main loop, to make .drv file
    with open(RFM_DIR+"/src/"+fname,"w+") as file:
        for idx, label in enumerate(labels.keys()):
            #print(label)
            file.write(f"{label} \n")
            file.write(f"  {labels[label]} \n")
            
        file.write("*END")
    file.close()
    
    
    
    
    