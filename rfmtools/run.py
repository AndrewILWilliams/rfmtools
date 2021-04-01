"""
A.W. 2021

Run the RFM.
"""


import numpy as np
import climlab
import xarray as xr
import subprocess
import io
import os
from .utils import RFM_DIR, read_spec


def run(drv_file = None, clean_files = False):
    """
    Run the RFM, make sure nothing gets overwritten, parse output directly to xarray!
    """
    
    cwd = os.getcwd()
    os.chdir(os.path.join(RFM_DIR, 'src'))
    
    # Run the model
    print("Running RFM...")
    process = subprocess.run([os.getcwd()+"/rfm"], capture_output=True)
    
    os.chdir(cwd) # back to initial dir
    
    #Check for errors!
    if process.stdout.split()[-2]==b'Successful':
        print("RFM run successful!")
    else:
        raise ValueError("RFM run unsuccessful, take a look at rfm.log")
        
    # Parse output to xarray
    # Assume simple 1d arrays for now...    
    fp = open(drv_file)
    for i, line in enumerate(fp):
        if line[0:4]=='*OUT':
            OUT_idx = i+1
        else:
            continue
    fp.close()

    fp = open(drv_file)
    parsed_outdir = fp.readlines()[OUT_idx].split()[-1]
    
    nu,_ = read_spec(parsed_outdir+"*")

    da = xr.DataArray(_, dims='wavenumber', coords={'wavenumber':nu})
    
    if clean_files:
        os.remove( parsed_outdir + '*')       # clean up tmp files
        os.rmdir( tmp_dir )
        
    return da



