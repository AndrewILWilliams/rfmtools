import numpy as np
import climlab
import xarray as xr


# Define functions, mostly just wrappers around climlab stuff

def qsat(T, P): 
    """Compute saturation specific humidity as function of temperature and pressure.

    Input:  T is temperature in Kelvin
            p is pressure in hPa or mb
    Output: saturation specific humidity (dimensionless).
    """
    return climlab.utils.thermo.qsat(T, P)


def pseudoadiabat(T,p):
    """
    Pressure coords gives dT/dP (if using the T/P prefactor, else dlnT/dlnP)
    """
    return climlab.utils.thermo.pseudoadiabat(T, p)


def dry_adiabat(T,P):
    return np.divide(params.R_a, params.cp_a)
