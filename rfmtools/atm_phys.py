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


def planck_wavenumber(nu,T):
    """
    Returns in W/m2/m
    """
    import scipy.constants
    h = scipy.constants.h
    pi = scipy.constants.pi
    c = scipy.constants.c
    kb = scipy.constants.Boltzmann
    u = h*nu/(kb*T)
    return 2.*pi*(kb*T)**3/((h*c)**2) * u**3/(np.exp(u)-1.)


def planck_nu(n,T,unit="cm^-1"):
    """
    Based on Ray's book.
    NOTE: Returns the radiance in W/m2/[length]
    where [length] is the unit in which I'm measuring the spectral axis.

    Conversion factor 'k' is necessary because Planck_wavenumber (above) returns
    """
    import scipy.constants
    h = scipy.constants.h
    c = scipy.constants.c
    kb = scipy.constants.Boltzmann
    if unit=="m^-1":
        k = 1.
    elif unit=="cm^-1":
        n = n*100.
        k = 100.
    else:
        print( "(planck_nu) Error: unit not recognized!")
    return k*c*planck_wavenumber(n*c,T)
