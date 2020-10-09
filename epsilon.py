import numpy as np
import params
from numba import njit
import matplotlib.pyplot as pl
#from matplotlib import patches
#from scipy.integrate import ode
#from scipy.special import erf
#from sys import exit
from matplotlib import rc
rc("text", usetex=False)

def initial_condition_spinorbit(y0,e_fermi,temperature,bandstruct,i_k,dynamics_type):
    e_v = bandstruct[i_k,1]
    e_c = bandstruct[i_k,2]
    if (temperature > 1e-5):
        fermi_function_e_c = 1/(np.exp((e_c-e_fermi)/temperature)+1)
        fermi_function_e_v = 1/(np.exp((e_v-e_fermi)/temperature)+1)
        y0.extend([fermi_function_e_v,0.0,0.0,fermi_function_e_c,0.0,0.0,0.0,0.0])
    else:
        if (e_c>e_fermi):
            y0_e_plus = 0
        else:
            y0_e_plus = 1

        if (e_v>e_fermi):
            y0_e_minus = 0
        else:
            y0_e_minus = 1

        y0.extend([y0_e_minus,0.0,0.0,y0_e_plus,0.0,0.0,0.0,0.0])


def epsilon(Nk_in_Path, path, dk, E_dir):
    beta = params.beta                                            #strength of H_diag
    gamma = params.gamma*params.angstr_conv**3           #strength of H_SO, units: eV 
    length = -path[0,0]
    a = params.a
    print(length)
    print(dk)
    print(np.pi/params.a)
    bandstruct = np.zeros(shape=(Nk_in_Path,3))
    bandstruct[:,0] = np.arange(-length, length+dk, dk)
   
    k_x     = (bandstruct[:,0])
    k_y     = (path[0,1])

    if params.structure_type == "zinc-blende":
        bandstruct[:,1] = params.eV_conv*(beta*(np.cos(k_x*a)+np.cos(k_y*a)) - 0.5*gamma*np.sqrt((k_x**4*k_y**2+k_x**2*k_y**4)))           # e_minus or e_v
        bandstruct[:,2] = params.eV_conv*(beta*(np.cos(k_x*a)+np.cos(k_y*a)) + 0.5*gamma*np.sqrt((k_x**4*k_y**2+k_x**2*k_y**4)))           # e_plus or e_c
        
    if params.structure_type == "wurtzite":
        alpha = params.alpha_wz*params.angstr_conv
        bandstruct[:,1] = params.eV_conv*(beta*(np.cos(k_x*a)+np.cos(k_y*a)) - 0.5*np.sqrt((alpha-gamma*(k_x**2+k_y**2))**2*(k_x**2+k_y**2))) # e_minus
        bandstruct[:,2] = params.eV_conv*(beta*(np.cos(k_x*a)+np.cos(k_y*a)) + 0.5*np.sqrt((alpha-gamma*(k_x**2+k_y**2))**2*(k_x**2+k_y**2))) # e_plus  

    return bandstruct

def epsilon_diff(Nk_in_Path, path, dk, E_dir):
    beta = params.beta                                            #strength of H_diag
    gamma = params.gamma*params.angstr_conv**3           #strength of H_SO, units: eV 
    length = -path[0,0]
    a = params.a

    band_diff_x = np.zeros(shape=(Nk_in_Path,3))
    band_diff_y = np.zeros(shape=(Nk_in_Path,3))
    band_diff_x[:,0] = np.arange(-length, length+dk, dk)
    band_diff_y[:,0] = np.arange(-length, length+dk, dk)
   
    k_x     = band_diff_x[:,0]
    k_y     = path[0,1]

    if params.structure_type == "zinc-blende":
        band_diff_x[:,1] = params.eV_conv*(-beta*a*np.sin(k_x*a) - 0.5*gamma*(2*k_x**2+k_y**2)*(k_x*k_y**2)/np.sqrt(k_x**4*k_y**2+k_x**2*k_y**4))

        band_diff_x[:,2] = params.eV_conv*(-beta*a*np.sin(k_x*a) + 0.5*gamma*(2*k_x**2+k_y**2)*(k_x*k_y**2)/np.sqrt(k_x**4*k_y**2+k_x**2*k_y**4))
        

        band_diff_y[:,1] = params.eV_conv*(-beta*a*np.sin(k_y*a) - 0.5*gamma*(k_x**2+2*k_y**2)*(k_x**2*k_y)/np.sqrt(k_x**4*k_y**2+k_x**2*k_y**4))

        band_diff_y[:,2] = params.eV_conv*(-beta*a*np.sin(k_y*a) + 0.5*gamma*(k_x**2+2*k_y**2)*(k_x**2*k_y)/np.sqrt(k_x**4*k_y**2+k_x**2*k_y**4))
    if params.structure_type == "wurtzite":
        alpha = params.alpha_wz*params.angstr_conv
       
        band_diff_x[:,1] = params.eV_conv*(-beta*a*np.sin(k_x*a) - 0.5*(k_x*(gamma*(k_x**2+k_y**2)-alpha)**2+(k_x**2+k_y**2)*(gamma*(k_x**2+k_y**2)-alpha)*2*k_x*gamma)/np.sqrt((k_x**2+k_y**2)*(gamma*(k_x**2+k_y**2)-alpha)**2))

        band_diff_x[:,2] = params.eV_conv*(-beta*a*np.sin(k_x*a) + 0.5*(k_x*(gamma*(k_x**2+k_y**2)-alpha)**2+(k_x**2+k_y**2)*(gamma*(k_x**2+k_y**2)-alpha)*2*k_x*gamma)/np.sqrt((k_x**2+k_y**2)*(gamma*(k_x**2+k_y**2)-alpha)**2))

        
        band_diff_y[:,1] = params.eV_conv*(-beta*a*np.sin(k_y*a) - 0.5*(k_y*(gamma*(k_x**2+k_y**2)-alpha)**2+(k_x**2+k_y**2)*(gamma*(k_x**2+k_y**2)-alpha)*2*k_y*gamma)/np.sqrt((k_x**2+k_y**2)*(gamma*(k_x**2+k_y**2)-alpha)**2))
        band_diff_y[:,2] = params.eV_conv*(-beta*a*np.sin(k_y*a) + 0.5*(k_y*(gamma*(k_x**2+k_y**2)-alpha)**2+(k_x**2+k_y**2)*(gamma*(k_x**2+k_y**2)-alpha)*2*k_y*gamma)/np.sqrt((k_x**2+k_y**2)*(gamma*(k_x**2+k_y**2)-alpha)**2))
    return band_diff_x, band_diff_y



def dipole(kx, ky):
    Nk_in_Path  =   params.Nk_in_path
    d       = 0.5*ky/(kx**2+ky**2)
    dy      = 0.5*kx/(kx**2+ky**2)
    #part1   = np.ones(Nk_in_Path, dtype=np.complex128)
    #part0   = np.zeros(Nk_in_Path, dtype=np.complex128)
    #di_x    = np.concatenate((part0,part1,part1,part0)).reshape(2,2,Nk_in_Path)
    di_x    = np.concatenate((-d,d,d,-d)).reshape(2,2,Nk_in_Path)
    di_y    = np.concatenate((dy,-dy,-dy,dy)).reshape(2,2,Nk_in_Path)
    di_y    = di_y.astype('complex128')
    return di_x, di_y



