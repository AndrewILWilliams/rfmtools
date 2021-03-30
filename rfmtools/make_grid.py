"""
A.W. 2021

Set of functions to generate idealized temperature/pressure/height/H2O 
fields to input into RFM.
"""

import numpy as np
import climlab
import xarray as xr
from .atm_phys import pseudoadiabat, qsat


def _get_height_array(htop=60e3, dz=200):
    """
    Height field from surface (0m) to htop(m) 
    in steps of dz (m)
    """
    return np.arange(0, htop, dz)


def _get_h2o_profile_dilute(temp=None, pres=None, RH=0.8, Tstrat=200):
    """
    Calculate 
    q = RH*qsat is only valid if water vapor is dilute!
    
    q[p<p_trop] = q_trop
    """
    q_base = RH*climlab.utils.thermo.qsat(temp, pres)

    # use interpolation to find p_trop, where T=Tstrat. Then compute q at that level.
    from scipy import interpolate
    p_trop = interpolate.interp1d(temp, pres)(Tstrat)
    q_trop = RH*climlab.utils.thermo.qsat(Tstrat,p_trop)
    
    mask = (pres<=p_trop)
    
    q = q_base
    q[mask] = q_trop        
    return q


def _get_temp_q_pres_from_height(height_array=None, Ts=300, Tstrat=200, ps=1e3, RH=0.8):
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
    temp = np.zeros(len(height_arr))
    pres = np.zeros(len(height_arr))

    temp[0] = Ts
    pres[0] = ps
    
    # Iterative solution
    for h_idx, height in enumerate(height_arr[:-1]):
        temp[h_idx+1] = temp[h_idx] - climlab.utils.thermo.pseudoadiabat(temp[h_idx], pres[h_idx])*(np.divide(g*pres[h_idx], params.R_a*temp[h_idx]))*dz
        pres[h_idx+1] = pres[h_idx] - g*np.divide(dz*pres[h_idx], params.R_a*temp[h_idx])
    
    # Calculate idealized profiles of temp, q
    # use interpolation to find p_trop, where T=Tstrat. Then compute q at that level.
    from scipy import interpolate
    p_trop = interpolate.interp1d(temp, pres)(Tstrat)
    mask = (pres<=p_trop)
    
    T = temp
    T[mask] = Tstrat

    # Idealized specific humidity profile
    q = _get_h2o_profile_dilute(temp, pres, RH, Tstrat)
    
    return T, q, pres

