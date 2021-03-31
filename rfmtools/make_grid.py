"""
A.W. 2021

Set of functions to generate idealized temperature/pressure/height/H2O 
fields to input into RFM.
"""

import numpy as np
import climlab
import xarray as xr
from .constants import R_a, g 

def _get_height_array(htop=60e3, dz=200):
    """
    Height field from surface (0m) to htop(m) 
    in steps of dz (m)
    """
    return np.arange(0, htop, dz)


def _get_h2o_profile_dilute(temp=None, pres=None, RH=0.8, Tstrat=200, ptrop=None):
    """
    Calculate 
    q = RH*qsat is only valid if water vapor is dilute!
    
    q[p<p_trop] = q_trop
    """
    q_base = RH*climlab.utils.thermo.qsat(temp, pres)

    if ptrop is not None:
        q_trop = RH*climlab.utils.thermo.qsat(Tstrat,ptrop)
        mask = (pres<=ptrop)
        q = q_base
        q[mask] = q_trop        
        return q
    else:
        return q_base
    
    
def _specific_humidity_to_ppmv(q, pres):
    wvp = climlab.utils.thermo.vapor_pressure_from_specific_humidity(pres, q)
    ppmv = np.divide(wvp, pres-wvp)*1e6
    return ppmv


def _get_temp_h2o_pres_from_height(height_array=None, Ts=300, Tstrat=200, ps=1e3, RH=0.8):
    """
    Generate idealized temperature, q and pressure arrays from height, 
    by integrating along moist adiabat assuming 
    hydrostatic atmosphere and ideal-gas law. 
    Also assumes water vapour is *dilute*!
    
    Iterative approach: T+1 = T + dTdP*dPdz*dz
                        p+1 = p + dPdz*dz

    Calculate 
    q = RH*qsat is only valid if water vapor is dilute!
    
    q[p<p_trop] = q_trop
    T[p<p_trop] = Tstrat
    
    Ts: surface temperature (K)
    Tstrat: stratosphere temperature (K)
    ps: surface pressure (hPa)
    """
    
    if height_array is None:
        height_array = _get_height_array()
        
    dz = (height_array[1]-height_array[0]) # m, assumed constant
    
    # Initialize arrays
    temp = np.zeros(len(height_array))
    pres = np.zeros(len(height_array))

    temp[0] = Ts
    pres[0] = ps
    
    # Iterative solution
    trop_idx = 0
    for h_idx, height in enumerate(height_array[:-1]):
        temp[h_idx+1] = temp[h_idx] - climlab.utils.thermo.pseudoadiabat(temp[h_idx], pres[h_idx])*(np.divide(g*pres[h_idx], R_a*temp[h_idx]))*dz
        pres[h_idx+1] = pres[h_idx] - g*np.divide(dz*pres[h_idx], R_a*temp[h_idx])
        
        if temp[h_idx]>Tstrat:
            temp[h_idx+1] = temp[h_idx] - climlab.utils.thermo.pseudoadiabat(temp[h_idx], pres[h_idx])*(np.divide(g*pres[h_idx], R_a*temp[h_idx]))*dz
            pres[h_idx+1] = pres[h_idx] - g*np.divide(dz*pres[h_idx], R_a*temp[h_idx])
        else:
            if trop_idx==0:
                ptrop = pres[h_idx]
                trop_idx+=1
                
            temp[h_idx+1] = Tstrat
            pres[h_idx+1] = pres[h_idx] - g*np.divide(dz*pres[h_idx], R_a*Tstrat)
        
        
    # Calculate idealized temp profile
    mask = (pres<=ptrop)
    
    T = temp
    T[mask] = Tstrat

    ## Idealized specific humidity profile
    q = _get_h2o_profile_dilute(temp, pres, RH, Tstrat, ptrop=ptrop)
    
    # Convert to ppmv h2o, as required by RFM
    ppmv = _specific_humidity_to_ppmv(q, pres)
    return T, ppmv, pres

