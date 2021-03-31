"""
A.W. 2021

Run the RFM.
"""


import numpy as np
import climlab
import xarray as xr
import subprocess
import os
from .utils import RFM_DIR 


def run():
    cwd = os.getcwd()
    os.chdir(os.path.join(RFM_DIR, 'src'))
    
    process = subprocess.run([os.getcwd()+"/rfm"], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
    
    os.chrdir(cwd)
    return 1



