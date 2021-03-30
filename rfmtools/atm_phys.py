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


def get_satvps(T):
    H2O_TriplePointT = 2.731500e+02 # K
    H2O_TriplePointP = 6.110000e+02 # hPa
    H2O_L_vaporization_TriplePoint = 2.493000e+06
    Rv = 461.5 #Jkg−1K−1
    return H2O_TriplePointP*np.exp(-(H2O_L_vaporization_TriplePoint/Rv)*(1./T - 1./H2O_TriplePointT))

def pseudoadiabat(T,p):
    """
    Pressure coords gives dT/dP (if using the T/P prefactor, else dlnT/dlnP)
    """
    return climlab.utils.thermo.pseudoadiabat(T, p)


def dry_adiabat(T,P):
    return np.divide(params.R_a, params.cp_a)
